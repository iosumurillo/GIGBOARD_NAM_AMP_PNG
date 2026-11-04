with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import struct

# The name string is at 0x15e3ff8.
# In ARM 32-bit ELF, its virtual address is 0x15e3ff8 + 0x8000 = 0x15ebff8.
# The typeinfo structure has:
# vtable ptr (_ZTVN10__cxxabiv117__class_type_infoE + 8 or similar)
# name ptr (0x15ebff8)
name_vaddr = 0x15ebff8
print(f"Searching for pointer to name 0x{name_vaddr:x}...")
matches = []
for i in range(0, len(data) - 4, 4):
    v = struct.unpack('<I', data[i:i+4])[0]
    if v == name_vaddr:
        matches.append(i)
print("Typeinfo at file offsets:", [hex(m) for m in matches])

for m in matches:
    # m is file offset of the pointer to name
    # typeinfo start is typically m - 4
    ti_vaddr = (m - 4) + 0x8000
    print(f"Typeinfo vaddr: 0x{ti_vaddr:x}")
    # Now find vtable pointing to ti_vaddr
    for j in range(0, len(data) - 4, 4):
        v = struct.unpack('<I', data[j:j+4])[0]
        if v == ti_vaddr:
            print(f"  Vtable ref at file offset: 0x{j:x} (vaddr: 0x{j+0x8000:x})")

