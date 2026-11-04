import re

with open('patch/nam_hook.cpp', 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize CRLF to LF for consistent handling
content = content.replace('\r\n', '\n')

# 1. sched.h
target1 = '#include <mutex>\n#include <pthread.h>\n#include <string>'
assert target1 in content, 'target1 not found'
content = content.replace(target1, '#include <mutex>\n#include <pthread.h>\n#include <sched.h>\n#include <string>')

# 2. lower_background_thread_priority
target2 = '''inline void lower_background_thread_priority()
{
  setpriority(PRIO_PROCESS, 0, 19); // 19 = lowest (nicest) niceness
}'''
assert target2 in content, 'target2 not found'
repl2 = '''inline void lower_background_thread_priority()
{
  struct sched_param sp;
  std::memset(&sp, 0, sizeof(sp));
  sched_setscheduler(0, SCHED_IDLE, &sp);
  setpriority(PRIO_PROCESS, 0, 19); // 19 = lowest (nicest) niceness
  nice(19);
}'''
content = content.replace(target2, repl2)

# 3. calibrate_slimmable_quality
target3 = '''    const auto t0 = std::chrono::steady_clock::now();
    for (int iter = 0; iter < kCalibrationIters; ++iter)
      dsp.process(in_arr, out_arr, kCalibrationBlockSize);
    const auto t1 = std::chrono::steady_clock::now();
    const double avg_us = static_cast<double>(
                             std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count())
                           / static_cast<double>(kCalibrationIters);'''
assert target3 in content, 'target3 not found'
repl3 = '''    int64_t total_us = 0;
    for (int iter = 0; iter < kCalibrationIters; ++iter)
    {
      const auto t0 = std::chrono::steady_clock::now();
      dsp.process(in_arr, out_arr, kCalibrationBlockSize);
      const auto t1 = std::chrono::steady_clock::now();
      total_us += std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
      usleep(500);
    }
    const double avg_us = static_cast<double>(total_us) / static_cast<double>(kCalibrationIters);'''
content = content.replace(target3, repl3)

# 4. switch_model_in_background: yield after nam::get_dsp
target4_1 = '''        d = nam::get_dsp(config);
        d->Reset(kSampleRate, 128); // establish sample rate/buffer size FIRST --'''
assert target4_1 in content, 'target4_1 not found'
repl4_1 = '''        d = nam::get_dsp(config);
        usleep(500);
        d->Reset(kSampleRate, 128); // establish sample rate/buffer size FIRST --'''
content = content.replace(target4_1, repl4_1)

# 4. switch_model_in_background: slice prewarming
target4_2 = '''          for (int32_t done = 0; done < kPrewarmSamples; done += kPrewarmBlockSize)
          {
            d->process(in_arr, out_arr, kPrewarmBlockSize);
            usleep(500);
          }'''
assert target4_2 in content, 'target4_2 not found'
repl4_2 = '''          constexpr int32_t kPrewarmSlice = 48;
          std::vector<float> silence48(kPrewarmSlice, 0.0f);
          std::vector<float> scratch48(kPrewarmSlice, 0.0f);
          float* in_arr48[1] = {silence48.data()};
          float* out_arr48[1] = {scratch48.data()};
          for (int32_t done = 0; done < kPrewarmSamples; done += kPrewarmSlice)
          {
            d->process(in_arr48, out_arr48, kPrewarmSlice);
            usleep(500);
          }'''
content = content.replace(target4_2, repl4_2)

# 5. nam_process_amp
idx_amp = content.find('// Original PreAmp process function in Evil (Gigboard 2.7)')
assert idx_amp != -1, 'idx_amp not found'
new_amp_code = '''// Original AmpCab process function in Evil (Gigboard 2.7)
typedef void (*amp_process_fn)(void*, uint32_t, float**, uint32_t, float**, int32_t, uint32_t*, void*);
static amp_process_fn orig_amp_process()
{
  static amp_process_fn fn = []() -> amp_process_fn {
    if (const char* env = std::getenv("NAM_ORIG_AMP_PROCESS_ADDR"))
    {
      uintptr_t addr = static_cast<uintptr_t>(std::strtoul(env, nullptr, 0));
      if (addr != 0)
        return reinterpret_cast<amp_process_fn>(addr);
    }
    return reinterpret_cast<amp_process_fn>(0x12b318);
  }();
  return fn;
}

extern "C" void nam_process_amp(void* this_, uint32_t param2, float** input, uint32_t numChannels,
                                float** output, int32_t numFrames, uint32_t* flags, void* ctx)
{
  flush_denormals_to_zero();
  if (numFrames <= 0 || !input || !output || numChannels == 0 || !this_)
    return;
  if (numChannels > kMaxChannels)
    numChannels = kMaxChannels;

  auto* self = reinterpret_cast<uint8_t*>(this_);

  // Inspect Amp Model Type (DSP ID) at offset 0x94ec
  const int32_t amp_type = *reinterpret_cast<int32_t*>(self + 0x94ec);
  if (amp_type != 27) // 27 = 0x1b = "82 LEAD 800 Bright"
  {
    orig_amp_process()(this_, param2, input, numChannels, output, numFrames, flags, ctx);
    return;
  }

  // Bypass handling at offset 0x95cc
  const uint8_t bypass_byte = *(self + 0x95cc);
  if (bypass_byte != 0)
  {
    for (uint32_t ch = 0; ch < numChannels; ++ch)
      if (input[ch] && output[ch])
        std::memcpy(output[ch], input[ch], static_cast<size_t>(numFrames) * sizeof(float));
    return;
  }

  auto& s = state_for(this_);
  const int32_t kFadeOutLenSamples = fade_out_len_samples();
  const int32_t kFadeInLenSamples = fade_in_len_samples();

  auto read_param = [self](size_t off, float def_val = 0.5f) -> float {
    float v = *reinterpret_cast<float*>(self + off);
    if (std::isnan(v) || std::isinf(v)) return def_val;
    if (v > 1.0f && v <= 100.0f) return v / 100.0f;
    return std::clamp(v, 0.0f, 1.0f);
  };

  // 9 Parameters on AmpCab:
  // 1. GainB -> NAM Model selector (0 .. N-1 dynamic steps)
  const float model_select_raw = read_param(0x9504, 0.5f);
  // 2. GainA -> Input Gain (trim_gain curve)
  const float gain_raw         = read_param(0x9500, 0.5f);
  // 3. Bright -> Tight Cut (HPF @ 720 Hz, Q=0.707)
  const bool bright_on         = (*(self + 0x9518) != 0) || (*reinterpret_cast<float*>(self + 0x9518) > 0.5f);
  // 4. Bass -> Bass (Low-Shelf @ 100 Hz, +/-12 dB)
  const float bass_raw         = read_param(0x952c, 0.5f);
  // 5. Mid -> Middle (Peaking @ MidFreq, +/-12 dB, Q=1.0)
  const float mid_raw          = read_param(0x9528, 0.5f);
  // 6. MidFreq -> Mid Freq (center frequency 200..5000 Hz)
  const float mid_freq_raw     = *reinterpret_cast<float*>(self + 0x950c);
  // 7. Treble -> Treble (High-Shelf @ 3500 Hz, +/-12 dB)
  const float treble_raw       = read_param(0x9524, 0.5f);
  // 8. Presence -> Presence (High-Shelf @ 6000 Hz, +/-10 dB)
  const float presence_raw     = read_param(0x9510, 0.3f);
  // 9. Master -> Output Lvl (master_gain = master_raw * 2.0f, clamped)
  const float master_raw       = read_param(0x9508, 0.5f);

  float mid_freq_hz = 1610.0f;
  if (!std::isnan(mid_freq_raw) && mid_freq_raw >= 200.0f && mid_freq_raw <= 5000.0f)
    mid_freq_hz = mid_freq_raw;
  else if (!std::isnan(mid_freq_raw) && mid_freq_raw > 0.0f && mid_freq_raw <= 1.0f)
    mid_freq_hz = 200.0f + mid_freq_raw * (5000.0f - 200.0f);

  // Configure active tone-stack filters
  for (uint32_t ch = 0; ch < numChannels; ++ch)
  {
    s.tone_bass[ch].set_low_shelf(static_cast<float>(kSampleRate), 100.0f, (bass_raw - 0.5f) * 24.0f);
    s.tone_mid[ch].set_peaking(static_cast<float>(kSampleRate), mid_freq_hz, (mid_raw - 0.5f) * 24.0f, 1.0f);
    s.tone_treble[ch].set_high_shelf(static_cast<float>(kSampleRate), 3500.0f, (treble_raw - 0.5f) * 24.0f);
    s.tone_presence[ch].set_high_shelf(static_cast<float>(kSampleRate), 6000.0f, (presence_raw - 0.5f) * 20.0f);
    if (bright_on)
      s.tight_boost[ch].set_high_pass(static_cast<float>(kSampleRate), 720.0f, 0.707f);
  }

  s.last_seen_knob_raw.store(model_select_raw, std::memory_order_release);
  bool ready = s.ready.load(std::memory_order_acquire);
  if (!ready)
  {
    switch_model_in_background(s, model_select_raw, s.force_recalibrate, true);
  }
  else
  {
    const int target_idx = knob_value_to_index(model_select_raw, static_cast<int>(g_cached_models.size()), true);
    if (target_idx != s.candidate_index)
    {
      s.candidate_index = target_idx;
      s.candidate_since_ms = now_ms();
    }
    else if (target_idx != -2 && target_idx != s.active_index.load(std::memory_order_acquire)
             && now_ms() - s.candidate_since_ms >= kKnobSettleMs)
    {
      if (s.fade_state.load(std::memory_order_relaxed) == 0)
      {
        s.fade_state.store(1, std::memory_order_relaxed);
        s.fade_progress = 0;
      }
    }

    if (s.fade_state.load(std::memory_order_relaxed) == 0 && s.active_index.load(std::memory_order_acquire) >= 0
        && s.calibrated_epoch.load(std::memory_order_acquire) != g_topology_epoch.load(std::memory_order_acquire))
    {
      s.force_recalibrate = true;
      s.fade_state.store(1, std::memory_order_relaxed);
      s.fade_progress = 0;
    }
  }

  if (s.fade_state.load(std::memory_order_relaxed) == 3 && !s.pending_ready.load(std::memory_order_acquire))
    switch_model_in_background(s, model_select_raw, s.force_recalibrate, true);

  const int fs_for_pickup = s.fade_state.load(std::memory_order_relaxed);
  if ((fs_for_pickup == 0 || fs_for_pickup == 3) && s.pending_ready.load(std::memory_order_acquire))
  {
    const int current_idx = knob_value_to_index(model_select_raw, static_cast<int>(g_cached_models.size()), true);
    const int pending = s.pending_index;
    if (pending != current_idx && current_idx != -2 && !s.force_recalibrate)
    {
      for (int i = 0; i < kMaxChannels; ++i)
        s.pending_dsp[i].reset();
      s.pending_ready.store(false, std::memory_order_release);
      s.fade_state.store(3, std::memory_order_relaxed);
      switch_model_in_background(s, model_select_raw, s.force_recalibrate, true);
    }
    else
    {
      for (int i = 0; i < kMaxChannels; ++i)
        s.dsp[i] = std::move(s.pending_dsp[i]);
      s.active_index.store(pending, std::memory_order_release);
      s.calibrated_epoch.store(g_topology_epoch.load(std::memory_order_acquire), std::memory_order_release);
      s.force_recalibrate = false;
      s.pending_ready.store(false, std::memory_order_release);
      s.ready.store(true, std::memory_order_release);
      if (fs_for_pickup == 3)
      {
        s.fade_state.store(pending < 0 ? 0 : 2, std::memory_order_relaxed);
        s.fade_progress = 0;
      }
    }
  }

  if (!ready || !s.dsp[0])
  {
    for (uint32_t ch = 0; ch < numChannels; ++ch)
      if (input[ch] && output[ch])
        std::memcpy(output[ch], input[ch], static_cast<size_t>(numFrames) * sizeof(float));
    return;
  }

  const float in_gain = trim_gain(gain_raw);
  const float master_gain = master_raw * 2.0f;

  // Pre-NAM conditioning: Input Gain + Tight Cut filter + Clamp
  for (uint32_t ch = 0; ch < numChannels; ++ch)
  {
    if (!input[ch] || !output[ch])
      continue;
    for (int32_t i = 0; i < numFrames; ++i)
    {
      float sample = input[ch][i] * in_gain;
      if (bright_on)
        sample = s.tight_boost[ch].process(sample);
      output[ch][i] = std::clamp(sample, -1.0f, 1.0f);
    }
  }

  const int fade_state = s.fade_state.load(std::memory_order_relaxed);
  const bool silent_active = s.active_index.load(std::memory_order_relaxed) < 0;

  if (fade_state == 0) // Steady state
  {
    for (uint32_t ch = 0; ch < numChannels; ++ch)
    {
      if (!input[ch] || !output[ch])
        continue;
      if (silent_active)
      {
        std::fill(output[ch], output[ch] + numFrames, 0.0f);
        continue;
      }
      float* in_arr[1] = {output[ch]};
      float* out_arr[1] = {output[ch]};
      s.dsp[ch]->process(in_arr, out_arr, numFrames);
    }
  }
  else if (fade_state == 1) // Fading OUT old model
  {
    for (uint32_t ch = 0; ch < numChannels; ++ch)
    {
      if (!input[ch] || !output[ch])
        continue;
      if (silent_active)
      {
        std::fill(output[ch], output[ch] + numFrames, 0.0f);
        continue;
      }
      float* in_arr[1] = {output[ch]};
      float* out_arr[1] = {output[ch]};
      s.dsp[ch]->process(in_arr, out_arr, numFrames);
      for (int32_t i = 0; i < numFrames; ++i)
      {
        const float g = 1.0f - raised_cosine_ramp(s.fade_progress + i, kFadeOutLenSamples);
        output[ch][i] *= g;
      }
    }
    s.fade_progress += numFrames;
    if (s.fade_progress >= kFadeOutLenSamples)
    {
      s.fade_progress = 0;
      const int current_idx = knob_value_to_index(model_select_raw, static_cast<int>(g_cached_models.size()), true);
      if (current_idx == s.active_index.load(std::memory_order_acquire) && !s.force_recalibrate)
      {
        s.fade_state.store(s.active_index.load(std::memory_order_relaxed) < 0 ? 0 : 2, std::memory_order_relaxed);
      }
      else
      {
        s.fade_state.store(3, std::memory_order_relaxed);
        switch_model_in_background(s, model_select_raw, s.force_recalibrate, true);
      }
    }
  }
  else if (fade_state == 3) // Muted wait while background thread loads
  {
    for (uint32_t ch = 0; ch < numChannels; ++ch)
      if (input[ch] && output[ch])
        std::fill(output[ch], output[ch] + numFrames, 0.0f);
  }
  else // fade_state == 2: Fading IN new model
  {
    for (uint32_t ch = 0; ch < numChannels; ++ch)
    {
      if (!input[ch] || !output[ch])
        continue;
      for (int32_t i = 0; i < numFrames; ++i)
        output[ch][i] *= raised_cosine_ramp(s.fade_progress + i, kFadeInLenSamples);

      float* in_arr[1] = {output[ch]};
      float* out_arr[1] = {output[ch]};
      s.dsp[ch]->process(in_arr, out_arr, numFrames);

      for (int32_t i = 0; i < numFrames; ++i)
      {
        const float g = raised_cosine_ramp(s.fade_progress + i, kFadeInLenSamples);
        output[ch][i] *= g;
      }
    }
    s.fade_progress += numFrames;
    if (s.fade_progress >= kFadeInLenSamples)
    {
      s.fade_progress = 0;
      s.fade_state.store(0, std::memory_order_relaxed);
    }
  }

  // Post-NAM conditioning: Active 3-Band EQ + Presence + Master Volume + Clamp
  for (uint32_t ch = 0; ch < numChannels; ++ch)
  {
    if (!input[ch] || !output[ch])
      continue;
    for (int32_t i = 0; i < numFrames; ++i)
    {
      float sample = output[ch][i];
      sample = s.tone_bass[ch].process(sample);
      sample = s.tone_mid[ch].process(sample);
      sample = s.tone_treble[ch].process(sample);
      sample = s.tone_presence[ch].process(sample);
      output[ch][i] = std::clamp(sample * master_gain, -1.0f, 1.0f);
    }
  }
}
'''
content = content[:idx_amp] + new_amp_code

with open('patch/nam_hook.cpp', 'w', encoding='utf-8') as f:
    f.write(content)
print('Successfully updated patch/nam_hook.cpp!')

