with open('/mnt/c/Antigravity/HEADRUSH/scratch/NAM_A2_pedal_exact.png', 'rb') as f:
    data = f.read()

assert len(data) == 75435

with open('/mnt/c/Antigravity/HEADRUSH/core/anxiety_od_png_patch.h', 'w') as f:
    f.write('/* Auto-generated NAM A2 pedal PNG patch (75435 bytes) */\n')
    f.write('#ifndef ANXIETY_OD_PNG_PATCH_H\n')
    f.write('#define ANXIETY_OD_PNG_PATCH_H\n\n')
    f.write('#include <stddef.h>\n#include <stdint.h>\n\n')
    f.write('#define ANXIETY_OD_PNG_PATCH_LEN 75435\n\n')
    f.write('static const uint8_t ANXIETY_OD_PNG_PATCH[ANXIETY_OD_PNG_PATCH_LEN] = {\n')
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_str = ','.join(f'0x{b:02x}' for b in chunk)
        f.write(f'  {hex_str},\n')
    f.write('};\n\n')
    f.write('#endif /* ANXIETY_OD_PNG_PATCH_H */\n')

print("Wrote core/anxiety_od_png_patch.h successfully!")

