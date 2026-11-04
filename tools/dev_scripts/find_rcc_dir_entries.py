with open('/mnt/c/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct

# In Qt RCC, let's find the tree node for the directory "img" inside "Pages/ModuleEditors"
# The name "img" is at 0x298d4de.
# In the tree, a directory node has:
# name_offset (4 bytes)
# flags (2 bytes) = 0x0001 (Directory)
# child_count (4 bytes)
# child_offset (4 bytes) - index into the tree!
# Let's search for who references the name of "img"!
# Where is "img" at 0x298d4de?
# Let's search for name offsets in tree:
# Let's test all possible tree entries that have child_count around 95 (since there are 95 images in this dir)!
for off in range(0x2900000, 0x2960000, 4):
    cnt = struct.unpack_from('>I', evil, off)[0]
    if 85 <= cnt <= 110:
        # Check if off-6 or off-4 has flags == 1
        flags1 = struct.unpack_from('>H', evil, off-2)[0]
        flags2 = struct.unpack_from('>H', evil, off-6)[0]
        print(f"Candidate dir with count={cnt} at {hex(off)}: flags1={flags1}, flags2={flags2}")
        print(f"Context: {evil[off-16:off+20].hex()}")

