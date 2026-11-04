with open('/mnt/c/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct

print("RCC nodes around 0x29442d0:")
for off in range(0x29442b0, 0x2944350, 14):
    entry = evil[off:off+14]
    name_off, flags, loc, child_or_data = struct.unpack('>IHHI', entry)
    print(f"{hex(off)}: name_off={hex(name_off)}, flags={flags}, loc={hex(loc)}, target={hex(child_or_data)}")

