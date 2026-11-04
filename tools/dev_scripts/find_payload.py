with open('/mnt/c/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct

# ActiveStomp.qml data is at 0x1852310.
# The 4 bytes before it: length = 15288 (0x00003bb8).
# In RCC, the data_offset in the tree points to the 4-byte length prefix!
# So target data address is 0x185230c!
# Let's search for who contains (0x185230c - payload_base)
# If data_offset is big-endian, let's search for values ending in 0x230c or 0x310
for off in range(0x1000000, 0x2a00000, 2):
    val_be = struct.unpack_from('>I', evil, off)[0]
    val_le = struct.unpack_from('<I', evil, off)[0]
    for v in (val_be, val_le):
        if (v & 0xfff) == 0x30c:
            # check if 0x185230c - v is consistent
            base = 0x185230c - v
            if 0x1500000 <= base <= 0x185230c:
                print(f"Match at {hex(off)}: val={hex(v)} -> payload base {hex(base)}")

