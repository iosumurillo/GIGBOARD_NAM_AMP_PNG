import struct

with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

e_phoff = struct.unpack('<I', data[28:32])[0]
e_phentsize = struct.unpack('<H', data[42:44])[0]
e_phnum = struct.unpack('<H', data[44:46])[0]

print(f"e_phnum={e_phnum}, e_phoff=0x{e_phoff:x}")
for i in range(e_phnum):
    off = e_phoff + i * e_phentsize
    p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_flags, p_align = struct.unpack('<IIIIIIII', data[off:off+32])
    print(f"PHDR {i}: type={p_type} off=0x{p_offset:x} vaddr=0x{p_vaddr:x} filesz=0x{p_filesz:x} memsz=0x{p_memsz:x} flags=0x{p_flags:x}")

