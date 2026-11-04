import re

with open(r'c:\Antigravity\HEADRUSH\patch\nam_hook.cpp', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Biquad struct before knob_value_to_index
biquad_code = '''struct Biquad
{
  float b0 = 1.0f, b1 = 0.0f, b2 = 0.0f;
  float a1 = 0.0f, a2 = 0.0f;
  float z1 = 0.0f, z2 = 0.0f;

  void reset()
  {
    z1 = 0.0f;
    z2 = 0.0f;
  }

  inline float process(float in)
  {
    float out = in * b0 + z1;
    z1 = in * b1 - out * a1 + z2;
    z2 = in * b2 - out * a2;
    return out;
  }

  void set_low_shelf(float sample_rate, float cutoff_hz, float gain_db)
  {
    if (std::abs(gain_db) < 0.05f)
    {
      b0 = 1.0f; b1 = 0.0f; b2 = 0.0f;
      a1 = 0.0f; a2 = 0.0f;
      return;
    }
    const float A = std::pow(10.0f, gain_db / 40.0f);
    const float w0 = 2.0f * static_cast<float>(M_PI) * cutoff_hz / sample_rate;
    const float cos_w = std::cos(w0);
    const float sin_w = std::sin(w0);
    const float alpha = sin_w / 2.0f * std::sqrt(2.0f);
    const float two_sqrt_A_alpha = 2.0f * std::sqrt(A) * alpha;

    const float a0 = (A + 1.0f) + (A - 1.0f) * cos_w + two_sqrt_A_alpha;
    b0 = (A * ((A + 1.0f) - (A - 1.0f) * cos_w + two_sqrt_A_alpha)) / a0;
    b1 = (2.0f * A * ((A - 1.0f) - (A + 1.0f) * cos_w)) / a0;
    b2 = (A * ((A + 1.0f) - (A - 1.0f) * cos_w - two_sqrt_A_alpha)) / a0;
    a1 = (-2.0f * ((A - 1.0f) + (A + 1.0f) * cos_w)) / a0;
    a2 = ((A + 1.0f) + (A - 1.0f) * cos_w - two_sqrt_A_alpha) / a0;
  }

  void set_high_shelf(float sample_rate, float cutoff_hz, float gain_db)
  {
    if (std::abs(gain_db) < 0.05f)
    {
      b0 = 1.0f; b1 = 0.0f; b2 = 0.0f;
      a1 = 0.0f; a2 = 0.0f;
      return;
    }
    const float A = std::pow(10.0f, gain_db / 40.0f);
    const float w0 = 2.0f * static_cast<float>(M_PI) * cutoff_hz / sample_rate;
    const float cos_w = std::cos(w0);
    const float sin_w = std::sin(w0);
    const float alpha = sin_w / 2.0f * std::sqrt(2.0f);
    const float two_sqrt_A_alpha = 2.0f * std::sqrt(A) * alpha;

    const float a0 = (A + 1.0f) - (A - 1.0f) * cos_w + two_sqrt_A_alpha;
    b0 = (A * ((A + 1.0f) - (A - 1.0f) * cos_w + two_sqrt_A_alpha)) / a0;
    b1 = (-2.0f * A * ((A - 1.0f) + (A + 1.0f) * cos_w)) / a0;
    b2 = (A * ((A + 1.0f) - (A - 1.0f) * cos_w - two_sqrt_A_alpha)) / a0;
    a1 = (2.0f * ((A - 1.0f) - (A + 1.0f) * cos_w)) / a0;
    a2 = ((A + 1.0f) - (A - 1.0f) * cos_w - two_sqrt_A_alpha) / a0;
  }

  void set_peaking(float sample_rate, float center_hz, float gain_db, float Q = 1.0f)
  {
    if (std::abs(gain_db) < 0.05f)
    {
      b0 = 1.0f; b1 = 0.0f; b2 = 0.0f;
      a1 = 0.0f; a2 = 0.0f;
      return;
    }
    const float A = std::pow(10.0f, gain_db / 40.0f);
    const float w0 = 2.0f * static_cast<float>(M_PI) * center_hz / sample_rate;
    const float cos_w = std::cos(w0);
    const float sin_w = std::sin(w0);
    const float alpha = sin_w / (2.0f * Q);

    const float a0 = 1.0f + alpha / A;
    b0 = (1.0f + alpha * A) / a0;
    b1 = (-2.0f * cos_w) / a0;
    b2 = (1.0f - alpha * A) / a0;
    a1 = (-2.0f * cos_w) / a0;
    a2 = (1.0f - alpha / A) / a0;
  }

  void set_high_pass(float sample_rate, float cutoff_hz, float Q = 0.707f)
  {
    const float w0 = 2.0f * static_cast<float>(M_PI) * cutoff_hz / sample_rate;
    const float cos_w = std::cos(w0);
    const float sin_w = std::sin(w0);
    const float alpha = sin_w / (2.0f * Q);

    const float a0 = 1.0f + alpha;
    b0 = ((1.0f + cos_w) / 2.0f) / a0;
    b1 = (-(1.0f + cos_w)) / a0;
    b2 = ((1.0f + cos_w) / 2.0f) / a0;
    a1 = (-2.0f * cos_w) / a0;
    a2 = (1.0f - alpha) / a0;
  }
};
'''

# Update knob_value_to_index
old_knob = '''int knob_value_to_index(float raw, int file_count)
{
  if (file_count <= 0)
    return -2;
  const float lo = knob_min();
  const float hi = knob_max();
  float t = (hi > lo) ? (raw - lo) / (hi - lo) : 0.0f;
  t = std::clamp(t, 0.0f, 1.0f);
  int step = static_cast<int>(t * static_cast<float>(kKnobSteps - 1) + 0.5f);
  step = std::clamp(step, 0, kKnobSteps - 1);
  return (step < file_count) ? step : -1;
}'''

new_knob = '''int knob_value_to_index(float raw, int file_count, bool dynamic_steps = false)
{
  if (file_count <= 0)
    return -2;
  const float lo = knob_min();
  const float hi = knob_max();
  float t = (hi > lo) ? (raw - lo) / (hi - lo) : 0.0f;
  t = std::clamp(t, 0.0f, 1.0f);
  if (dynamic_steps)
  {
    int step = static_cast<int>(t * static_cast<float>(file_count - 1) + 0.5f);
    return std::clamp(step, 0, file_count - 1);
  }
  int step = static_cast<int>(t * static_cast<float>(kKnobSteps - 1) + 0.5f);
  step = std::clamp(step, 0, kKnobSteps - 1);
  return (step < file_count) ? step : -1;
}'''

assert old_knob in content, "old_knob not found!"
content = content.replace(old_knob, biquad_code + '\n' + new_knob)

# 2. Add tone stack Biquads to ModelState
old_model_state = '''  // Which engine object (this_) this slot belongs to -- see state_for().
  std::atomic<void*> owner_this{nullptr};
};'''

new_model_state = '''  // Active 3-band Tone Stack + Presence + Tight Boost filters
  Biquad tone_bass[kMaxChannels];
  Biquad tone_mid[kMaxChannels];
  Biquad tone_treble[kMaxChannels];
  Biquad tone_presence[kMaxChannels];
  Biquad tight_boost[kMaxChannels];

  // Which engine object (this_) this slot belongs to -- see state_for().
  std::atomic<void*> owner_this{nullptr};
};'''

assert old_model_state in content, "old_model_state not found!"
content = content.replace(old_model_state, new_model_state)

# 3. Update switch_model_in_background to accept dynamic_steps
old_switch = '''void switch_model_in_background(ModelState& s, float raw, bool force_reload_same_model = false)'''
new_switch = '''void switch_model_in_background(ModelState& s, float raw, bool force_reload_same_model = false, bool dynamic_steps = false)'''
assert old_switch in content, "old_switch not found!"
content = content.replace(old_switch, new_switch)

old_spawn = '''  spawn_detached([&s, raw, force_reload_same_model]() {'''
new_spawn = '''  spawn_detached([&s, raw, force_reload_same_model, dynamic_steps]() {'''
assert old_spawn in content, "old_spawn not found!"
content = content.replace(old_spawn, new_spawn)

old_idx = '''      const int idx = knob_value_to_index(raw, static_cast<int>(g_cached_models.size()));'''
new_idx = '''      const int idx = knob_value_to_index(raw, static_cast<int>(g_cached_models.size()), dynamic_steps);'''
assert old_idx in content, "old_idx not found!"
content = content.replace(old_idx, new_idx)

# 4. Add nam_process_amp implementation
amp_impl = '''
// Original PreAmp process function in Evil (Gigboard 2.7)
typedef void (*preamp_process_fn)(void*, uint32_t, float**, uint32_t, float**, int32_t, uint32_t*, void*);
static preamp_process_fn g_orig_preamp_process = reinterpret_cast<preamp_process_fn>(0x2f4fe8);

extern "C" void nam_process_amp(void* this_, uint32_t param2, float** input, uint32_t numChannels,
                                float** output, int32_t numFrames, uint32_t* flags, void* ctx)
{
  flush_denormals_to_zero();
  if (numFrames <= 0 || !input || !output || numChannels == 0)
    return;
  if (numChannels > kMaxChannels)
    numChannels = kMaxChannels;

  auto& s = state_for(this_);
  const int32_t kFadeOutLenSamples = fade_out_len_samples();
  const int32_t kFadeInLenSamples = fade_in_len_samples();

  auto* self = reinterpret_cast<uint8_t*>(this_);

  // Safe parameter reader with normalization
  auto read_param = [self](size_t off, float def_val = 0.5f) -> float {
    float v = *reinterpret_cast<float*>(self + off);
    if (std::isnan(v) || std::isinf(v)) return def_val;
    if (v > 1.0f && v <= 100.0f) return v / 100.0f;
    return std::clamp(v, 0.0f, 1.0f);
  };

  const float model_select_raw = read_param(0x5e8, 0.5f); // GainB (NAM Model Select)
  const float gain_raw = read_param(0x5d4, 0.5f);         // GainA (Input Gain / Saturation)
  const float bass_raw = read_param(0x5ac, 0.5f);         // Bass (Low Shelf)
  const float mid_raw = read_param(0x584, 0.5f);          // Mid (Peaking Mid)
  const float mid_freq_raw = *reinterpret_cast<float*>(self + 0x598); // MidFreq (Hz)
  const float treble_raw = read_param(0x570, 0.5f);       // Treble (High Shelf)
  const float presence_raw = read_param(0x5c0, 0.3f);     // Presence (Poweramp High Shelf)
  const float master_raw = read_param(0x624, 0.5f);       // Master (Output Volume)
  const float bright_raw = *reinterpret_cast<float*>(self + 0x55c);
  const uint8_t bypass_byte = *(self + 0x26c);

  float mid_freq_hz = 1610.0f;
  if (!std::isnan(mid_freq_raw) && mid_freq_raw >= 200.0f && mid_freq_raw <= 5000.0f)
    mid_freq_hz = mid_freq_raw;
  else if (!std::isnan(mid_freq_raw) && mid_freq_raw > 0.0f && mid_freq_raw <= 1.0f)
    mid_freq_hz = 200.0f + mid_freq_raw * (5000.0f - 200.0f);

  const bool bright_on = (bright_raw > 0.5f);

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

  // Bypass handling
  if (bypass_byte != 0)
  {
    for (uint32_t ch = 0; ch < numChannels; ++ch)
      if (input[ch] && output[ch])
        std::memcpy(output[ch], input[ch], static_cast<size_t>(numFrames) * sizeof(float));
    return;
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

    float* in_arr[1] = {output[ch]};
    float* out_arr[1] = {output[ch]};
    s.dsp[ch]->process(in_arr, out_arr, numFrames);

    // Apply Active 3-Band EQ + Presence + Master Volume
    for (int32_t i = 0; i < numFrames; ++i)
    {
      float sample = output[ch][i];
      sample = s.tone_bass[ch].process(sample);
      sample = s.tone_mid[ch].process(sample);
      sample = s.tone_treble[ch].process(sample);
      sample = s.tone_presence[ch].process(sample);
      output[ch][i] = sample * master_gain;
    }
  }
}
'''

content += amp_impl

with open(r'c:\Antigravity\HEADRUSH\patch\nam_hook.cpp', 'w', encoding='utf-8') as f:
    f.write(content)

print("patch_hook.py applied successfully!")

