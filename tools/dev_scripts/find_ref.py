with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct
for off in range(0x298da90, 0x298daa0):
    for base in [0x2987c58, 0x2980000, 0, 0x2987c58 + 0x8000]:
        val = off - base
        if val > 0:
            for fmt in ['>I', '<I']:
                b = struct.pack(fmt, val)
                pos = 0x2980000
                while True:
                    pos = evil.find(b, pos)
                    if pos == -1 or pos >= 0x2996000: break
                    print(f'Match at 0x{pos:x} for val=0x{val:x} ({fmt}) base=0x{base:x} off=0x{off:x}')
                    pos += 1
