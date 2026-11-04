with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

# In ARM code, let's search for string offset of "GainB" or "sld8"
# 0x15e2764 has sld7, GainA, sld8, GainB...
# Let's see the addresses:
# sld7 is at 0x15e2730
# GainA is at 0x15e2748
# sld8 is at 0x15e2760
# GainB is at 0x15e2778
# Let's search for references to 0x15e2778 + 0x8000 = 0x15ea778 or similar
target = 0x15ea778
import struct
for i in range(0, len(data)-4, 4):
    v = struct.unpack('<I', data[i:i+4])[0]
    if 0x15ea700 <= v <= 0x15ea800:
        print(f"Ref at {hex(i)} -> {hex(v)}")

