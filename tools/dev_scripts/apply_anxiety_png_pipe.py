with open('/mnt/c/Antigravity/HEADRUSH/core/patch_pipeline.c', 'rb') as f:
    content = f.read()

# Add include
include_target = b'#include "active_stomp_patch.h"\n'
include_repl = b'#include "active_stomp_patch.h"\n#include "anxiety_od_png_patch.h"\n'
if b'\r\n' in content:
    include_target = include_target.replace(b'\n', b'\r\n')
    include_repl = include_repl.replace(b'\n', b'\r\n')

assert include_target in content, "include_target not found!"
content = content.replace(include_target, include_repl, 1)

# Add patch logic
patch_target = b'''    if (!invalidated_qv4_unit)
    {
      report(progress, progress_user_data, "    (QV4 ActiveStomp bytecode header needle not found, skipped)");
    }
  }'''

patch_repl = b'''    if (!invalidated_qv4_unit)
    {
      report(progress, progress_user_data, "    (QV4 ActiveStomp bytecode header needle not found, skipped)");
    }

    /* Replace Anxiety OD pedal PNG with custom "NAM A2" artwork */
    static const uint8_t anxiety_png_needle[] = {
      0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52,
      0x00, 0x00, 0x01, 0x1e, 0x00, 0x00, 0x01, 0xba, 0x08, 0x06, 0x00, 0x00, 0x00, 0xde, 0x44, 0x29,
      0x2e, 0x00, 0x01, 0x26, 0x72, 0x49, 0x44, 0x41, 0x54, 0x78, 0x01, 0xec, 0xd4, 0xb5, 0x01, 0x02
    };
    bool patched_anxiety_png = false;
    for (size_t i = 0; i + sizeof(anxiety_png_needle) + ANXIETY_OD_PNG_PATCH_LEN <= evil_len; ++i)
    {
      if (memcmp(evil_data + i, anxiety_png_needle, sizeof(anxiety_png_needle)) == 0)
      {
        memcpy(evil_data + i, ANXIETY_OD_PNG_PATCH, ANXIETY_OD_PNG_PATCH_LEN);
        report(progress, progress_user_data, "OK  Anxiety OD PNG replaced with custom NAM A2 artwork @ 0x%zx", i);
        patched_anxiety_png = true;
        break;
      }
    }
    if (!patched_anxiety_png)
    {
      report(progress, progress_user_data, "    (Anxiety OD PNG needle not found, skipped)");
    }
  }'''

if b'\r\n' in content:
    patch_target = patch_target.replace(b'\n', b'\r\n')
    patch_repl = patch_repl.replace(b'\n', b'\r\n')

assert patch_target in content, "patch_target not found!"
content = content.replace(patch_target, patch_repl, 1)

with open('/mnt/c/Antigravity/HEADRUSH/core/patch_pipeline.c', 'wb') as f:
    f.write(content)

print("Successfully updated core/patch_pipeline.c with NAM A2 artwork patch!")

