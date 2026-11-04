with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import struct

target = 0x15ebff8
matches = []
for i in range(0, len(data) - 4, 4):
    v = struct.unpack('<I', data[i:i+4])[0]
    if v == target:
        matches.append(i)
print("Typeinfo matches for AmpCabController:", [hex(m) for m in matches])

