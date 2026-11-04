with open('core/patch_pipeline.c', 'rb') as f:
    content = f.read()

target_inc = b'#include "anxiety_od_png_patch.h"'
repl_inc = b'#include "anxiety_od_png_patch.h"\n#include "anxiety_od_v2_png_patch.h"'
if b'\r\n' in content:
    repl_inc = repl_inc.replace(b'\n', b'\r\n')

assert target_inc in content
content = content.replace(target_inc, repl_inc, 1)

target_patch = b'''    if (!patched_anxiety_png)
    {
      report(progress, progress_user_data, "    (Anxiety OD PNG needle not found, skipped)");
    }'''

repl_patch = b'''    if (!patched_anxiety_png)
    {
      report(progress, progress_user_data, "    (Anxiety OD PNG needle not found, skipped)");
    }

    /* Replace Anxiety OD V2 pedal PNG with custom "NAM A2" artwork */
    static const uint8_t anxiety_v2_png_needle[] = {
      0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52,
      0x00, 0x00, 0x01, 0x1e, 0x00, 0x00, 0x01, 0xb4, 0x08, 0x06, 0x00, 0x00, 0x00, 0xe4, 0x4e, 0x48,
      0x5e, 0x00, 0x00, 0xf5, 0xfe, 0x49, 0x44, 0x41, 0x54, 0x78, 0x01, 0xec, 0xd4, 0x01, 0x01, 0x00
    };
    bool patched_anxiety_v2_png = false;
    for (size_t i = 0; i + sizeof(anxiety_v2_png_needle) + ANXIETY_OD_V2_PNG_PATCH_LEN <= evil_len; ++i)
    {
      if (memcmp(evil_data + i, anxiety_v2_png_needle, sizeof(anxiety_v2_png_needle)) == 0)
      {
        memcpy(evil_data + i, ANXIETY_OD_V2_PNG_PATCH, ANXIETY_OD_V2_PNG_PATCH_LEN);
        report(progress, progress_user_data, "OK  Anxiety OD V2 PNG replaced with custom NAM A2 artwork @ 0x%zx", i);
        patched_anxiety_v2_png = true;
        break;
      }
    }
    if (!patched_anxiety_v2_png)
    {
      report(progress, progress_user_data, "    (Anxiety OD V2 PNG needle not found, skipped)");
    }'''

if b'\r\n' in content:
    target_patch = target_patch.replace(b'\n', b'\r\n')
    repl_patch = repl_patch.replace(b'\n', b'\r\n')

assert target_patch in content
content = content.replace(target_patch, repl_patch, 1)

with open('core/patch_pipeline.c', 'wb') as f:
    f.write(content)

print('Updated core/patch_pipeline.c successfully!')
