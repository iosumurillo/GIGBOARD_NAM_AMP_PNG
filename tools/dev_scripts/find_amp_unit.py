with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import struct

# In Qt Quick Compiler registration table:
# There is an array of structures:
# { const char* path; const char* qml_unit_data; } or similar
# Let's search for the pointer to 0x2d0f7f8 (vaddr = 0x2d0f7f8 + 0x8000 = 0x2d177f8)
# But wait, 0x2d0f7f8 is a QString object:
# QString object in Qt:
# struct Data { ref, size, alloc, capacityReserved, offset }
# The string data itself is at 0x2d0f818!
# Let's search for pointer to 0x2d0f808 (Data header) or 0x2d0f818 (string chars)!
for off in [0x2d0f7f8, 0x2d0f808, 0x2d0f818]:
    vaddr = off + 0x8000
    for i in range(0x2c00000, 0x3000000, 4):
        v = struct.unpack('<I', data[i:i+4])[0]
        if v == vaddr:
            print(f"Match for 0x{off:x} at 0x{i:x}")
            # print surrounding words
            for j in range(i-16, i+32, 4):
                val = struct.unpack('<I', data[j:j+4])[0]
                print(f"  0x{j:x}: 0x{val:x}")

