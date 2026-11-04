with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import struct

# Let's search for 0x1560ed8 (file offset of '82 LEAD 800 Bright\x00')
# In memory, vaddr is 0x1560ed8 + 0x8000 = 0x1568ed8
vaddr = 0x1568ed8

# Search for vaddr as a 32-bit integer everywhere
matches = []
for i in range(0, len(data) - 4, 4):
    v = struct.unpack('<I', data[i:i+4])[0]
    if v == vaddr:
        matches.append(i)

print(f"Matches for vaddr 0x{vaddr:x}: {[hex(m) for m in matches]}")

# Also search for relative or offset without 0x8000
matches_raw = []
for i in range(0, len(data) - 4, 4):
    v = struct.unpack('<I', data[i:i+4])[0]
    if v == 0x1560ed8:
        matches_raw.append(i)
print(f"Matches for 0x1560ed8: {[hex(m) for m in matches_raw]}")

