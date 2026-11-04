#!/usr/bin/env python3
import sys
import subprocess

def apply_variant(variant_name):
    valid = ['direct', 'rounded', 'knobs']
    if variant_name not in valid:
        print(f"Error: Unknown variant '{variant_name}'. Valid choices: {valid}")
        sys.exit(1)

    p1 = f'scratch/NAM_A2_{variant_name}_v1_exact.png'
    p2 = f'scratch/NAM_A2_{variant_name}_v2_exact.png'
    
    with open(p1, 'rb') as f: d1 = f.read()
    with open(p2, 'rb') as f: d2 = f.read()
    
    assert len(d1) == 75435, f"Length {len(d1)} != 75435"
    assert len(d2) == 63031, f"Length {len(d2)} != 63031"
    
    # Write core/anxiety_od_png_patch.h
    with open('core/anxiety_od_png_patch.h', 'w') as f:
        f.write(f'/* Auto-generated NAM A2 ({variant_name}) pedal PNG patch (75435 bytes) */\n')
        f.write('#ifndef ANXIETY_OD_PNG_PATCH_H\n#define ANXIETY_OD_PNG_PATCH_H\n\n')
        f.write('#include <stddef.h>\n#include <stdint.h>\n\n')
        f.write('#define ANXIETY_OD_PNG_PATCH_LEN 75435\n\n')
        f.write('static const uint8_t ANXIETY_OD_PNG_PATCH[ANXIETY_OD_PNG_PATCH_LEN] = {\n')
        for i in range(0, len(d1), 16):
            chunk = d1[i:i+16]
            f.write('  ' + ','.join(f'0x{b:02x}' for b in chunk) + ',\n')
        f.write('};\n\n#endif /* ANXIETY_OD_PNG_PATCH_H */\n')
        
    # Write core/anxiety_od_v2_png_patch.h
    with open('core/anxiety_od_v2_png_patch.h', 'w') as f:
        f.write(f'/* Auto-generated NAM A2 ({variant_name}) V2 pedal PNG patch (63031 bytes) */\n')
        f.write('#ifndef ANXIETY_OD_V2_PNG_PATCH_H\n#define ANXIETY_OD_V2_PNG_PATCH_H\n\n')
        f.write('#include <stddef.h>\n#include <stdint.h>\n\n')
        f.write('#define ANXIETY_OD_V2_PNG_PATCH_LEN 63031\n\n')
        f.write('static const uint8_t ANXIETY_OD_V2_PNG_PATCH[ANXIETY_OD_V2_PNG_PATCH_LEN] = {\n')
        for i in range(0, len(d2), 16):
            chunk = d2[i:i+16]
            f.write('  ' + ','.join(f'0x{b:02x}' for b in chunk) + ',\n')
        f.write('};\n\n#endif /* ANXIETY_OD_V2_PNG_PATCH_H */\n')

    print(f"[+] Successfully wrote C headers for variant: {variant_name}!")

if __name__ == '__main__':
    v = sys.argv[1] if len(sys.argv) > 1 else 'direct'
    apply_variant(v)

