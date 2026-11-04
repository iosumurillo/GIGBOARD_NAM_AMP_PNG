with open('/mnt/c/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct

for p in range(0x2988000, 0x298a500):
    l = struct.unpack_from('>H', evil, p)[0]
    if 1 <= l <= 30:
        chars = evil[p+6:p+6+l*2]
        if all(chars[i] == 0 and 32 <= chars[i+1] <= 126 for i in range(0, l*2, 2)):
            print(f'Possible names table start at {hex(p)}: len={l}, name={chars.decode("utf-16be")}')
            break

