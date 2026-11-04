/* patch_pipeline.c -- see patch_pipeline.h. */
#include "patch_pipeline.h"

#include "active_stomp_patch.h"
#include "anxiety_od_png_patch.h"
#include "user_art_patch.h"
#include "elf_patch.h"
#include "ext4_image.h"
#include "fit_image.h"
#include "launcher_script.h"
#include "model_targets.h"
#include "nam_blobs_embedded.h"
#include "qml_patch.h"
#include "xz_codec.h"

#include <errno.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void set_err(char* err, size_t err_size, const char* fmt, ...)
{
  if (!err || err_size == 0)
    return;
  va_list ap;
  va_start(ap, fmt);
  vsnprintf(err, err_size, fmt, ap);
  va_end(ap);
}

static void report(NamProgressFn progress, void* user_data, const char* fmt, ...)
{
  if (!progress)
    return;
  char buf[512];
  va_list ap;
  va_start(ap, fmt);
  vsnprintf(buf, sizeof(buf), fmt, ap);
  va_end(ap);
  progress(buf, user_data);
}

static uint8_t* read_whole_file_or_null(const char* path, size_t* out_len, char* err, size_t err_size)
{
  FILE* f = fopen(path, "rb");
  if (!f)
  {
    set_err(err, err_size, "opening %s: %s", path, strerror(errno));
    return NULL;
  }
  fseek(f, 0, SEEK_END);
  long sz = ftell(f);
  fseek(f, 0, SEEK_SET);
  if (sz < 0)
  {
    set_err(err, err_size, "ftell %s failed", path);
    fclose(f);
    return NULL;
  }
  uint8_t* buf = (uint8_t*)malloc((size_t)sz ? (size_t)sz : 1);
  if (!buf)
  {
    set_err(err, err_size, "out of memory reading %s (%ld bytes)", path, sz);
    fclose(f);
    return NULL;
  }
  if (sz > 0 && fread(buf, 1, (size_t)sz, f) != (size_t)sz)
  {
    set_err(err, err_size, "short read on %s", path);
    free(buf);
    fclose(f);
    return NULL;
  }
  fclose(f);
  *out_len = (size_t)sz;
  return buf;
}

static bool write_whole_file(const char* path, const uint8_t* data, size_t len, char* err, size_t err_size)
{
  FILE* f = fopen(path, "wb");
  if (!f)
  {
    set_err(err, err_size, "opening %s for write: %s", path, strerror(errno));
    return false;
  }
  bool ok = (len == 0) || (fwrite(data, 1, len, f) == len);
  fclose(f);
  if (!ok)
    set_err(err, err_size, "short write on %s", path);
  return ok;
}

bool nam_patch_pipeline(const uint8_t* stock_img_data, size_t stock_img_len, const char* model_name,
                         bool enable_v2_hijack, const char* workdir, NamProgressFn progress, void* progress_user_data,
                         uint8_t** out_img_data, size_t* out_img_len, char* err, size_t err_size)
{
  *out_img_data = NULL;
  *out_img_len = 0;

  FitProps props = {0};
  FitProps verify_props = {0};
  bool props_valid = false, verify_props_valid = false;
  uint8_t* rootfs_bin = NULL;
  uint8_t* evil_data = NULL;
  uint8_t* script_data_raw = NULL;
  char* script_data = NULL;
  char* new_script = NULL;
  uint8_t* rootfs_patched = NULL;
  uint8_t* rootfs_patched_xz = NULL;
  uint8_t* out_fit = NULL;
  uint8_t* verify_rootfs_bin = NULL;
  uint8_t* verify_evil = NULL;
  Ext4Image* img = NULL;
  Ext4Image* verify_img = NULL;
  bool ok = false;

  if (!nam_fit_parse(stock_img_data, stock_img_len, &props))
  {
    set_err(err, err_size, "doesn't look like a valid FIT image (bad FDT magic?)");
    goto cleanup;
  }
  props_valid = true;

  FitMetadata metadata;
  if (!nam_fit_read_root_metadata(stock_img_data, &props, &metadata))
  {
    set_err(err, err_size, "FIT root node is missing description/compatible/inmusic,devices");
    goto cleanup;
  }
  report(progress, progress_user_data, "OK  extracted metadata: description=%s compatible=%s", metadata.description,
         metadata.compatible);

  const char* reason;
  const ModelTarget* target = nam_select_target(model_name, metadata.compatible, &reason);
  if (!target)
  {
    set_err(err, err_size, "%s", reason);
    goto cleanup;
  }
  if (reason)
    report(progress, progress_user_data, "OK  model target: %s  (%s)", target->name, reason);
  else
    report(progress, progress_user_data, "OK  model target: %s", target->name);

  uint32_t splash_off, splash_len, recov_off, recov_len, rootfs_off, rootfs_len;
  if (!nam_fit_get_bytes(&props, "//images/splash", "data", &splash_off, &splash_len)
      || !nam_fit_get_bytes(&props, "//images/recoverysplash", "data", &recov_off, &recov_len)
      || !nam_fit_get_bytes(&props, "//images/rootfs", "data", &rootfs_off, &rootfs_len))
  {
    set_err(err, err_size, "FIT image missing an expected splash/recoverysplash/rootfs image node");
    goto cleanup;
  }
  const uint8_t* splash_xz = stock_img_data + splash_off;
  const uint8_t* recoverysplash_xz = stock_img_data + recov_off;
  const uint8_t* rootfs_xz = stock_img_data + rootfs_off;
  report(progress, progress_user_data, "OK  extracted splash (%uB), recoverysplash (%uB), rootfs.xz (%uB)",
         splash_len, recov_len, rootfs_len);

  size_t rootfs_bin_len;
  if (!nam_xz_decompress(rootfs_xz, rootfs_len, &rootfs_bin, &rootfs_bin_len, err, err_size))
    goto cleanup;

  char rootfs_path[600];
  snprintf(rootfs_path, sizeof(rootfs_path), "%s/rootfs.bin", workdir);
  if (!write_whole_file(rootfs_path, rootfs_bin, rootfs_bin_len, err, err_size))
    goto cleanup;
  free(rootfs_bin);
  rootfs_bin = NULL;

  if (!nam_ext4_open(rootfs_path, true, &img, err, err_size))
    goto cleanup;

  size_t evil_len;
  if (!nam_ext4_dump(img, "/usr/Evil/Evil", &evil_data, &evil_len, err, err_size))
    goto cleanup;

  size_t script_len;
  if (!nam_ext4_dump(img, "/usr/Evil/Scripts/evil", &script_data_raw, &script_len, err, err_size))
    goto cleanup;
  script_data = (char*)malloc(script_len + 1);
  if (!script_data)
  {
    set_err(err, err_size, "out of memory");
    goto cleanup;
  }
  memcpy(script_data, script_data_raw, script_len);
  script_data[script_len] = '\0';
  free(script_data_raw);
  script_data_raw = NULL;

  const uint8_t* tramp = g_nam_trampoline_gonk_bin;
  size_t tramp_len = (size_t)g_nam_trampoline_gonk_bin_len;
  if (tramp_len != 32)
  {
    set_err(err, err_size, "embedded trampoline_gonk.bin is %zu bytes, expected exactly 32", tramp_len);
    goto cleanup;
  }

  ElfPatchResult elf_result;
  if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->engine_vtable_vaddr, target->orig_process_fn, 8u,
                                 &elf_result, err, err_size))
    goto cleanup;
  report(progress, progress_user_data, "OK  ELF hijack patched: trampoline @ 0x%x, hook_slot @ 0x%x",
         elf_result.trampoline_vaddr, elf_result.hook_slot_addr);

  ElfPatchResult elf_result_v2;
  bool has_v2_hijack = false;
  if (enable_v2_hijack)
  {
    if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->v2_engine_vtable_vaddr,
                                   target->v2_orig_process_fn, 8u, &elf_result_v2, err, err_size))
      goto cleanup;
    has_v2_hijack = true;
    report(progress, progress_user_data, "OK  ELF hijack patched (Anxiety OD V2): trampoline @ 0x%x, hook_slot @ 0x%x",
           elf_result_v2.trampoline_vaddr, elf_result_v2.hook_slot_addr);
  }

  ElfPatchResult elf_result_amp;
  bool has_amp_hijack = false;
  if (target->amp_engine_vtable_vaddr != 0 && target->amp_orig_process_fn != 0)
  {
    if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->amp_engine_vtable_vaddr,
                                   target->amp_orig_process_fn,
                                   target->amp_process_slot ? target->amp_process_slot : 7u,
                                   &elf_result_amp, err, err_size))
      goto cleanup;
    has_amp_hijack = true;
    report(progress, progress_user_data, "OK  ELF hijack patched (Amp LEAD 800 Bright): trampoline @ 0x%x, hook_slot @ 0x%x",
           elf_result_amp.trampoline_vaddr, elf_result_amp.hook_slot_addr);
  }

  if (target->qml_rename_count > 0)
  {
    if (!nam_qml_patch(evil_data, evil_len, target, err, err_size))
      goto cleanup;
    report(progress, progress_user_data, "OK  QML knob labels relabeled");
  }
  else
  {
    report(progress, progress_user_data, "    (QML knob relabel skipped for %s -- no per-pedal target)",
           target->name);
  }

  /* Patch ActiveStomp.qml to replace generic colored blocks with pedal artwork */
  {
    const uint8_t needle[] = {0x00, 0x00, 0x3b, 0xb8, 0x78, 0x9c};
    size_t needle_len = sizeof(needle);
    bool patched_artwork = false;
    for (size_t i = 0; i + needle_len + ACTIVE_STOMP_PATCH_LEN <= evil_len; ++i)
    {
      if (memcmp(evil_data + i, needle, needle_len) == 0)
      {
        memcpy(evil_data + i + 4, ACTIVE_STOMP_PATCH, ACTIVE_STOMP_PATCH_LEN);
        report(progress, progress_user_data, "OK  ActiveStomp.qml patched with realistic pedal artwork @ 0x%zx", i + 4);
        patched_artwork = true;
        break;
      }
    }
    if (!patched_artwork)
    {
      report(progress, progress_user_data, "    (ActiveStomp.qml artwork needle not found, skipped)");
    }

    /* Bypass Qt Quick Compiler (QV4) cache for ActiveStomp.qml so Qt loads patched RCC */
    static const uint8_t qv4_path_needle[] = {
      '/', 0, 'G', 0, 'r', 0, 'o', 0, 'u', 0, 'p', 0, 's', 0, '/', 0,
      'S', 0, 'i', 0, 'g', 0, 'n', 0, 'a', 0, 'l', 0, 'C', 0, 'h', 0, 'a', 0, 'i', 0, 'n', 0,
      'M', 0, 'o', 0, 'd', 0, 'u', 0, 'l', 0, 'e', 0, 'S', 0, 't', 0, 'o', 0, 'm', 0, 'p', 0, 's', 0, '/', 0,
      'A', 0, 'c', 0, 't', 0, 'i', 0, 'v', 0, 'e', 0, 'S', 0, 't', 0, 'o', 0, 'm', 0, 'p', 0,
      '.', 0, 'q', 0, 'm', 0, 'l', 0
    };
    bool bypassed_qv4_path = false;
    for (size_t i = 0; i + sizeof(qv4_path_needle) <= evil_len; ++i)
    {
      if (memcmp(evil_data + i, qv4_path_needle, sizeof(qv4_path_needle)) == 0)
      {
        /* Invalidate registration path: /Groups/.../ActiveStomp -> /Groups/.../XctiveStomp */
        /* 'A' is at byte offset 64 */
        evil_data[i + 64] = 'X';
        report(progress, progress_user_data, "OK  Bypassed QV4 compiled unit registration @ 0x%zx", i);
        bypassed_qv4_path = true;
        break;
      }
    }
    if (!bypassed_qv4_path)
    {
      report(progress, progress_user_data, "    (QV4 ActiveStomp registration needle not found, skipped)");
    }

    /* Also invalidate unit header magic if found so verifyHeader fails */
    static const uint8_t qv4_header_needle[] = {
      'q', 'v', '4', 'c', 'd', 'a', 't', 'a',
      0x29, 0x00, 0x00, 0x00, 0x02, 0x0f, 0x05, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
      0x84, 0xd8, 0x00, 0x00
    };
    bool invalidated_qv4_unit = false;
    for (size_t i = 0; i + sizeof(qv4_header_needle) <= evil_len; ++i)
    {
      if (memcmp(evil_data + i, qv4_header_needle, sizeof(qv4_header_needle)) == 0)
      {
        evil_data[i + 3] = 'x'; /* qv4xdata */
        report(progress, progress_user_data, "OK  Invalidated QV4 ActiveStomp compiled bytecode @ 0x%zx", i);
        invalidated_qv4_unit = true;
        break;
      }
    }
    if (!invalidated_qv4_unit)
    {
      report(progress, progress_user_data, "    (QV4 ActiveStomp bytecode header needle not found, skipped)");
    }

    /* Replace Anxiety OD and Anxiety OD V2 pedal PNGs with custom NAM badge artwork */
    static const uint8_t anxiety_png_needle[] = {
      0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52,
      0x00, 0x00, 0x01, 0x1e, 0x00, 0x00, 0x01, 0xba, 0x08, 0x06, 0x00, 0x00, 0x00, 0xde, 0x44, 0x29,
      0x2e, 0x00, 0x01, 0x26, 0xc6, 0x49, 0x44, 0x41, 0x54, 0x78, 0xda, 0xec, 0xd6
    };
    int patched_anxiety_png_count = 0;
    for (size_t i = 0; i + sizeof(anxiety_png_needle) + ANXIETY_OD_PNG_PATCH_LEN <= evil_len; ++i)
    {
      if (memcmp(evil_data + i, anxiety_png_needle, sizeof(anxiety_png_needle)) == 0)
      {
        memcpy(evil_data + i, ANXIETY_OD_PNG_PATCH, ANXIETY_OD_PNG_PATCH_LEN);
        report(progress, progress_user_data, "OK  Anxiety OD PNG #%d replaced with custom NAM badge artwork @ 0x%zx",
               patched_anxiety_png_count + 1, i);
        patched_anxiety_png_count++;
      }
    }
    if (patched_anxiety_png_count == 0)
    {
      report(progress, progress_user_data, "    (Anxiety OD PNG needle not found, skipped)");
    }

    /* Replace 82 LEAD 800 Bright Amp PNGs with custom artwork */
    if (has_amp_hijack)
    {
      if (AMP_A_OFF + AMP_A_LEN <= evil_len && memcmp(evil_data + AMP_A_OFF, AMP_A_NEEDLE, sizeof(AMP_A_NEEDLE)) == 0)
      {
        memcpy(evil_data + AMP_A_OFF, AMP_A_PNG, AMP_A_LEN);
        report(progress, progress_user_data, "OK  82 LEAD 800 Bright Amp PNG #1 replaced with custom artwork @ 0x%x", AMP_A_OFF);
      }
      if (AMP_B_OFF + AMP_B_LEN <= evil_len && memcmp(evil_data + AMP_B_OFF, AMP_B_NEEDLE, sizeof(AMP_B_NEEDLE)) == 0)
      {
        memcpy(evil_data + AMP_B_OFF, AMP_B_PNG, AMP_B_LEN);
        report(progress, progress_user_data, "OK  82 LEAD 800 Bright Amp PNG #2 replaced with custom artwork @ 0x%x", AMP_B_OFF);
      }
    }
  }

  char hook_slot_hex[32];
  snprintf(hook_slot_hex, sizeof(hook_slot_hex), "0x%x", elf_result.hook_slot_addr);
  char hook_slot_v2_hex[32];
  if (has_v2_hijack)
    snprintf(hook_slot_v2_hex, sizeof(hook_slot_v2_hex), "0x%x", elf_result_v2.hook_slot_addr);
  char hook_slot_amp_hex[32];
  if (has_amp_hijack)
    snprintf(hook_slot_amp_hex, sizeof(hook_slot_amp_hex), "0x%x", elf_result_amp.hook_slot_addr);
  if (!nam_build_launcher_script(script_data, hook_slot_hex, has_v2_hijack ? hook_slot_v2_hex : NULL,
                                  has_amp_hijack ? hook_slot_amp_hex : NULL, &new_script,
                                  err, err_size))
    goto cleanup;
  free(script_data);
  script_data = NULL;

  if (!nam_ext4_inject(img, "/usr/Evil/Evil", evil_data, evil_len, 0755, err, err_size))
    goto cleanup;

  const uint8_t* hook_so = g_nam_hook_so;
  size_t hook_so_len = (size_t)g_nam_hook_so_len;
  const uint8_t* preload_so = g_nam_preload_so;
  size_t preload_so_len = (size_t)g_nam_preload_so_len;

  if (!nam_ext4_inject(img, "/usr/Evil/libnam_hook.so", hook_so, hook_so_len, 0755, err, err_size))
    goto cleanup;
  if (!nam_ext4_inject(img, "/usr/Evil/libnam_preload.so", preload_so, preload_so_len, 0755, err, err_size))
    goto cleanup;
  if (!nam_ext4_inject(img, "/usr/Evil/Scripts/evil", (const uint8_t*)new_script, strlen(new_script), 0755, err,
                        err_size))
    goto cleanup;

  if (has_amp_hijack)
  {
    uint8_t* db_data = NULL;
    size_t db_len = 0;
    char db_err[256] = {0};
    if (nam_ext4_dump(img, "/usr/Evil/Content/evil.db", &db_data, &db_len, db_err, sizeof(db_err)) && db_data)
    {
      static const char kDbNeedle[] =
        "\"Presence\":{\"type\":0,\"value\":30},\"Treble\":{\"type\":0,\"value\":50},"
        "\"TremDepth\":{\"type\":0,\"value\":85},\"TremSpeed\":{\"type\":0,\"value\":6},"
        "\"TremSync\":{\"state\":false,\"type\":1},\"Tremolo\":{\"state\":false,\"type\":1},"
        "\"Type\":{\"string\":\"82 LEAD 800 Bright";
      static const char kDbReplacement[] =
        "\"Presence\":{\"type\":0,\"value\":50},\"Treble\":{\"type\":0,\"value\":50},"
        "\"TremDepth\":{\"type\":0,\"value\":50},\"TremSpeed\":{\"type\":0,\"value\":6},"
        "\"TremSync\":{\"state\":false,\"type\":1},\"Tremolo\":{\"state\":false,\"type\":1},"
        "\"Type\":{\"string\":\"82 LEAD 800 Bright";
      const size_t kDbNeedleLen = sizeof(kDbNeedle) - 1;
      bool db_patched = false;
      for (size_t i = 0; i + kDbNeedleLen <= db_len; ++i)
      {
        if (db_data[i] == '"' && memcmp(db_data + i, kDbNeedle, kDbNeedleLen) == 0)
        {
          memcpy(db_data + i, kDbReplacement, kDbNeedleLen);
          db_patched = true;
          break;
        }
      }
      if (db_patched && nam_ext4_inject(img, "/usr/Evil/Content/evil.db", db_data, db_len, 0644, db_err, sizeof(db_err)))
      {
        report(progress, progress_user_data, "OK  normalized +82 LEAD 800 BRIGHT preset defaults to 50 in evil.db");
      }
      free(db_data);
    }
  }

  report(progress, progress_user_data,
         "OK  injected patched Evil, libnam_hook.so, libnam_preload.so, launcher script");

  if (!nam_ext4_verify_basic(img, err, err_size))
    goto cleanup;
  report(progress, progress_user_data, "OK  ext4 self-consistency check passed");

  nam_ext4_close(img);
  img = NULL;
  free(new_script);
  new_script = NULL;

  size_t rootfs_patched_len;
  rootfs_patched = read_whole_file_or_null(rootfs_path, &rootfs_patched_len, err, err_size);
  if (!rootfs_patched)
    goto cleanup;

  size_t rootfs_patched_xz_len;
  if (!nam_xz_compress(rootfs_patched, rootfs_patched_len, &rootfs_patched_xz, &rootfs_patched_xz_len, err, err_size))
    goto cleanup;

  size_t out_fit_len;
  if (!nam_fit_build(&metadata, splash_xz, splash_len, recoverysplash_xz, recov_len, rootfs_patched_xz,
                      rootfs_patched_xz_len, &out_fit, &out_fit_len))
  {
    set_err(err, err_size, "building output FIT image (out of memory?)");
    goto cleanup;
  }
  report(progress, progress_user_data, "OK  built patched Update.img (%zu bytes)", out_fit_len);

  /* ---- round-trip verification ---- */
  if (!nam_fit_parse(out_fit, out_fit_len, &verify_props))
  {
    set_err(err, err_size, "round-trip FAILED: couldn't re-parse the FIT image we just wrote");
    goto cleanup;
  }
  verify_props_valid = true;

  uint32_t verify_rootfs_off, verify_rootfs_xz_len;
  if (!nam_fit_get_bytes(&verify_props, "//images/rootfs", "data", &verify_rootfs_off, &verify_rootfs_xz_len))
  {
    set_err(err, err_size, "round-trip FAILED: rebuilt FIT is missing the rootfs image node");
    goto cleanup;
  }

  size_t verify_rootfs_bin_len;
  if (!nam_xz_decompress(out_fit + verify_rootfs_off, verify_rootfs_xz_len, &verify_rootfs_bin,
                          &verify_rootfs_bin_len, err, err_size))
    goto cleanup;

  char verify_rootfs_path[600];
  snprintf(verify_rootfs_path, sizeof(verify_rootfs_path), "%s/verify_rootfs.bin", workdir);
  if (!write_whole_file(verify_rootfs_path, verify_rootfs_bin, verify_rootfs_bin_len, err, err_size))
    goto cleanup;
  free(verify_rootfs_bin);
  verify_rootfs_bin = NULL;

  if (!nam_ext4_open(verify_rootfs_path, false, &verify_img, err, err_size))
    goto cleanup;

  size_t verify_evil_len;
  if (!nam_ext4_dump(verify_img, "/usr/Evil/Evil", &verify_evil, &verify_evil_len, err, err_size))
    goto cleanup;

  if (verify_evil_len != evil_len || memcmp(verify_evil, evil_data, evil_len) != 0)
  {
    set_err(err, err_size, "round-trip FAILED: repacked Update.img's Evil binary doesn't match what was built");
    goto cleanup;
  }
  report(progress, progress_user_data, "OK  round-trip verified: repacked image's /usr/Evil/Evil is byte-exact");

  *out_img_data = out_fit;
  *out_img_len = out_fit_len;
  out_fit = NULL; /* ownership transferred to caller */
  ok = true;

cleanup:
  if (props_valid)
    nam_fit_props_free(&props);
  if (verify_props_valid)
    nam_fit_props_free(&verify_props);
  if (img)
    nam_ext4_close(img);
  if (verify_img)
    nam_ext4_close(verify_img);
  free(rootfs_bin);
  free(evil_data);
  free(script_data_raw);
  free(script_data);
  free(new_script);
  free(rootfs_patched);
  free(rootfs_patched_xz);
  free(out_fit);
  free(verify_rootfs_bin);
  free(verify_evil);
  return ok;
}
