with open('scratch/nam_badge_v1_exact.png', 'rb') as f:
    d1 = f.read()

with open('scratch/nam_badge_v2_exact.png', 'rb') as f:
    d2 = f.read()

assert len(d1) == 75435, f"V1 length {len(d1)} != 75435"
assert len(d2) == 63031, f"V2 length {len(d2)} != 63031"

with open('core/anxiety_od_png_patch.h', 'w') as f:
    f.write('/* Auto-generated NAM pedal badge PNG patch (75435 bytes) */\n')
    f.write('#ifndef ANXIETY_OD_PNG_PATCH_H\n#define ANXIETY_OD_PNG_PATCH_H\n\n')
    f.write('#include <stddef.h>\n#include <stdint.h>\n\n')
    f.write('#define ANXIETY_OD_PNG_PATCH_LEN 75435\n\n')
    f.write('static const uint8_t ANXIETY_OD_PNG_PATCH[ANXIETY_OD_PNG_PATCH_LEN] = {\n')
    for i in range(0, len(d1), 16):
        chunk = d1[i:i+16]
        f.write('  ' + ','.join(f'0x{b:02x}' for b in chunk) + ',\n')
    f.write('};\n\n#endif /* ANXIETY_OD_PNG_PATCH_H */\n')

with open('core/anxiety_od_v2_png_patch.h', 'w') as f:
    f.write('/* Auto-generated NAM pedal badge V2 PNG patch (63031 bytes) */\n')
    f.write('#ifndef ANXIETY_OD_V2_PNG_PATCH_H\n#define ANXIETY_OD_V2_PNG_PATCH_H\n\n')
    f.write('#include <stddef.h>\n#include <stdint.h>\n\n')
    f.write('#define ANXIETY_OD_V2_PNG_PATCH_LEN 63031\n\n')
    f.write('static const uint8_t ANXIETY_OD_V2_PNG_PATCH[ANXIETY_OD_V2_PNG_PATCH_LEN] = {\n')
    for i in range(0, len(d2), 16):
        chunk = d2[i:i+16]
        f.write('  ' + ','.join(f'0x{b:02x}' for b in chunk) + ',\n')
    f.write('};\n\n#endif /* ANXIETY_OD_V2_PNG_PATCH_H */\n')

print("Updated core/anxiety_od_png_patch.h and core/anxiety_od_v2_png_patch.h with NAM badge!")

