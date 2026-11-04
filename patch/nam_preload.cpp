// nam_preload.cpp -- tiny LD_PRELOAD shim.
//
// Loaded before /usr/Evil/Evil starts (set LD_PRELOAD=/usr/Evil/libnam_preload.so
// in evil.service or runevil), this constructor dlopen()s libnam_hook.so and
// wires up whichever hook(s) are configured (each independently, via its own
// env var -- see below), writing the resolved function pointer into the
// corresponding trampoline's hook_slot (injected by patch_evil.py /
// patch_gonkulator.py).
//
// Evil is non-PIE / no ASLR (confirmed: ELF type EXEC, pic=false), so hook_slot
// addresses are fixed, reproducible vaddrs across runs -- no runtime lookup
// needed.
//
// CURRENT (additive) design: NAM_HOOK_SLOT_NAML_ADDR -> nam_process_naml,
// NAM_HOOK_SLOT_NAML_TRIM_IN_ADDR -> nam_set_input_trim,
// NAM_HOOK_SLOT_NAML_TRIM_OUT_ADDR -> nam_set_output_trim (all three from
// patch_namloader.py's injected segment). Current SHIPPING design:
// NAM_HOOK_SLOT_GONK_ADDR -> nam_process_gonk (Anxiety OD v1 hijack) and,
// in the optional "up to 4 instances" build, NAM_HOOK_SLOT_GONK_V2_ADDR ->
// the SAME nam_process_gonk (Anxiety OD V2 hijack -- distinct vtable slot,
// same hook function, since it dispatches per-instance internally).
// SUPERSEDED designs, kept only as reference/fallback: the "Gonkulator"
// name above is historical (see nam_hook.cpp's file header) and
// NAM_HOOK_SLOT_ADDR -> nam_process (IRLoader hook -- overwrites real .wav
// IR loading everywhere).
// Only set a superseded design's env var if you deliberately want that old
// behavior back; see nam_hook.cpp's file header for why each was rejected.

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <dlfcn.h>
#include <string_view>
#include <unistd.h>

#define NAM_HOOK_LIB_PATH "/usr/Evil/libnam_hook.so"
#define EXPECTED_EXE_PATH "/usr/Evil/Evil"

namespace
{

// Ensure the "+82 LEAD 800 BRIGHT" default preset in /media/az01-internal/Evil/evil.db
// (copied from /usr/Evil/evil.db on first boot) initializes Presence and TremDepth to 50
// (equilibrium / 0 dB) instead of 30 and 85. In-place same-length replacement.
void normalize_amp_defaults_in_db(const char* db_path)
{
  static const char kNeedle[] =
    "\"Presence\":{\"type\":0,\"value\":30},\"Treble\":{\"type\":0,\"value\":50},"
    "\"TremDepth\":{\"type\":0,\"value\":85},\"TremSpeed\":{\"type\":0,\"value\":6},"
    "\"TremSync\":{\"state\":false,\"type\":1},\"Tremolo\":{\"state\":false,\"type\":1},"
    "\"Type\":{\"string\":\"82 LEAD 800 Bright";
  static const char kReplacement[] =
    "\"Presence\":{\"type\":0,\"value\":50},\"Treble\":{\"type\":0,\"value\":50},"
    "\"TremDepth\":{\"type\":0,\"value\":50},\"TremSpeed\":{\"type\":0,\"value\":6},"
    "\"TremSync\":{\"state\":false,\"type\":1},\"Tremolo\":{\"state\":false,\"type\":1},"
    "\"Type\":{\"string\":\"82 LEAD 800 Bright";
  constexpr size_t kLen = sizeof(kNeedle) - 1;

  FILE* f = std::fopen(db_path, "r+b");
  if (!f)
    return;
  if (std::fseek(f, 0, SEEK_END) != 0)
  {
    std::fclose(f);
    return;
  }
  const long sz = std::ftell(f);
  if (sz <= static_cast<long>(kLen) || sz > 16 * 1024 * 1024)
  {
    std::fclose(f);
    return;
  }
  std::fseek(f, 0, SEEK_SET);
  auto* buf = static_cast<char*>(std::malloc(static_cast<size_t>(sz)));
  if (!buf)
  {
    std::fclose(f);
    return;
  }
  if (std::fread(buf, 1, static_cast<size_t>(sz), f) == static_cast<size_t>(sz))
  {
    for (size_t i = 0; i + kLen <= static_cast<size_t>(sz); ++i)
    {
      if (buf[i] == '"' && std::memcmp(buf + i, kNeedle, kLen) == 0)
      {
        if (std::fseek(f, static_cast<long>(i), SEEK_SET) == 0)
        {
          std::fwrite(kReplacement, 1, kLen, f);
          std::fflush(f);
          fsync(fileno(f));
        }
        break;
      }
    }
  }
  std::free(buf);
  std::fclose(f);
}

// LD_PRELOAD (and the NAM_HOOK_SLOT_* env vars) are set only for the
// /usr/Evil/Evil exec itself, but environment variables are inherited by
// EVERY child process a program forks/execs, not just the one they were
// meant for. If Evil itself shells out to any helper (e.g. for USB mass-
// storage/file-transfer plumbing), that helper inherits these vars too,
// and this library's constructor would run inside it as well. The
// NAM_HOOK_SLOT_* addresses are hardcoded absolute addresses valid ONLY
// inside Evil's own non-PIE memory layout -- writing them into an unrelated
// process is at best a no-op, at worst a crash in that process. Refuse to
// touch anything unless we can confirm we're actually running inside the
// genuine, patched Evil binary.
bool running_inside_evil()
{
  char buf[64];
  ssize_t n = readlink("/proc/self/exe", buf, sizeof(buf) - 1);
  if (n <= 0)
    return false;
  buf[n] = '\0';
  return std::string_view(buf) == EXPECTED_EXE_PATH;
}

// Installs one hook: dlsym `sym_name` from `lib`, write it into the hook_slot
// whose address comes from env var `env_name` (skipped entirely if unset --
// no fallback default, since guessing wrong here silently no-ops the hook
// instead of crashing, which is much harder to notice).
void install_one_hook(void* lib, const char* sym_name, const char* env_name)
{
  const char* env = getenv(env_name);
  if (!env)
  {
    fprintf(stderr, "[nam_preload] %s not set, skipping %s hook\n", env_name, sym_name);
    return;
  }

  void* sym = dlsym(lib, sym_name);
  if (!sym)
  {
    fprintf(stderr, "[nam_preload] dlsym(%s) failed: %s\n", sym_name, dlerror());
    return;
  }

  const uintptr_t slot_addr = static_cast<uintptr_t>(strtoul(env, nullptr, 0));
  volatile auto* slot = reinterpret_cast<volatile uintptr_t*>(slot_addr);
  *slot = reinterpret_cast<uintptr_t>(sym);

  fprintf(stderr, "[nam_preload] hook installed: %s slot@0x%lx = %p\n",
          sym_name, static_cast<unsigned long>(slot_addr), sym);
}

} // namespace

__attribute__((constructor)) static void install_nam_hooks()
{
  if (!running_inside_evil())
  {
    fprintf(stderr, "[nam_preload] not running as " EXPECTED_EXE_PATH
                    " (inherited LD_PRELOAD in some other process?) -- skipping entirely\n");
    return;
  }

  normalize_amp_defaults_in_db("/media/az01-internal/Evil/Content/evil.db");
  normalize_amp_defaults_in_db("/media/az01-internal/Evil/evil.db");
  normalize_amp_defaults_in_db("/usr/Evil/Content/evil.db");
  normalize_amp_defaults_in_db("/usr/Evil/evil.db");

  void* lib = dlopen(NAM_HOOK_LIB_PATH, RTLD_NOW | RTLD_GLOBAL);
  if (!lib)
  {
    fprintf(stderr, "[nam_preload] dlopen(%s) failed: %s\n", NAM_HOOK_LIB_PATH, dlerror());
    return;
  }

  install_one_hook(lib, "nam_process_naml", "NAM_HOOK_SLOT_NAML_ADDR");
  install_one_hook(lib, "nam_set_input_trim", "NAM_HOOK_SLOT_NAML_TRIM_IN_ADDR");
  install_one_hook(lib, "nam_set_output_trim", "NAM_HOOK_SLOT_NAML_TRIM_OUT_ADDR");
  install_one_hook(lib, "nam_process_gonk", "NAM_HOOK_SLOT_GONK_ADDR");
  // Anxiety OD V2's hijack, for the optional "up to 4 instances" mode --
  // same compiled hook function as v1 (nam_process_gonk already dispatches
  // per-instance by engine-object pointer, see state_for() in nam_hook.cpp,
  // so it doesn't matter which pedal class' vtable slot called in). Skipped
  // entirely (see install_one_hook) when the 2-instance build didn't patch
  // a V2 hook_slot, so this env var is simply unset.
  install_one_hook(lib, "nam_process_gonk", "NAM_HOOK_SLOT_GONK_V2_ADDR");
  install_one_hook(lib, "nam_process_amp", "NAM_HOOK_SLOT_AMP_ADDR");
  install_one_hook(lib, "nam_process", "NAM_HOOK_SLOT_ADDR");

  // The one-time *.nam model preload (nam_hook.cpp's
  // preload_models_in_background) is deliberately NOT triggered from here.
  // Tried TWICE now, both reverted:
  //   1. Called unconditionally from here, synchronously doing the actual
  //      scan -- made the USB-transfer view hang worse (every boot, not just
  //      boots that engaged Anxiety OD).
  //   2. Called from here via nam_preload_models() (still exported, unused
  //      now), which only kicks off preload_models_in_background()'s
  //      spawn_detached (a real pthread_create) -- NOT the scan itself doing
  //      anything synchronously slow, just spawning the thread. Confirmed on
  //      real hardware this broke boot entirely: relay clicking every ~500ms,
  //      stuck on the splash screen, never reaching the real UI -- a crash/
  //      respawn loop. This constructor runs via ld.so's DT_INIT_ARRAY
  //      processing, BEFORE Evil's own main() -- spawning a pthread that
  //      early, before whatever Evil's own startup expects to have already
  //      initialized, is evidently unsafe on this device's actual libc/
  //      threading stack (works fine on a desktop/QEMU test harness, which
  //      is how attempt #2 passed every test available pre-hardware).
  // Triggered lazily instead, from inside nam_hook.cpp itself the first time
  // the hijacked process() actually runs -- by which point Evil's own main
  // loop is unquestionably already up and running real-time audio.
}
