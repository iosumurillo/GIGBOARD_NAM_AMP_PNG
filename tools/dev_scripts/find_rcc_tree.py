with open('/mnt/c/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct

# In Qt, let's look at all candidate base addresses for names:
# A name offset is name_addr - names_base.
# Since Anxiety OD.png is at 0x298da92, name_offset = 0x298da92 - names_base.
# Also, tree nodes have name_offset as a 4-byte big-endian integer.
# If tree nodes are in evil, name_offset < 0x100000 (usually < 65536).
# Let's search for patterns in the tree area (e.g. 0x2970000 to 0x2988000):
print("Scanning for RCC tree nodes...")
# A file node typically has flags = 0x0000 or 0x0002 (uncompressed=0, compressed=2)
# and a data_offset.
for off in range(0x2960000, 0x2985000, 2):
    # Try reading 14-byte node: [name_off: 4] [flags: 2] [locale: 4] [data_off: 4]
    name_off, flags = struct.unpack_from('>IH', evil, off)
    if flags in (0, 1, 2) and name_off < 0x20000:
        # Check next node at off+14 or off+16
        for stride in (14, 16):
            n2, f2 = struct.unpack_from('>IH', evil, off + stride)
            if f2 in (0, 1, 2) and n2 < 0x20000:
                n3, f3 = struct.unpack_from('>IH', evil, off + stride*2)
                if f3 in (0, 1, 2) and n3 < 0x20000:
                    print(f"Found tree sequence at {hex(off)} with stride {stride}: name_off={hex(name_off)}, flags={flags}")
                    break
        else:
            continue
        break

