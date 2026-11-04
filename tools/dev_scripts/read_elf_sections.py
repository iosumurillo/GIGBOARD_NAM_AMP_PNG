import struct

with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    hdr = f.read(52)
    e_shoff, = struct.unpack('<I', hdr[32:36])
    e_shentsize, = struct.unpack('<H', hdr[46:48])
    e_shnum, = struct.unpack('<H', hdr[48:50])
    e_shstrndx, = struct.unpack('<H', hdr[50:52])
    print(f"shoff={hex(e_shoff)}, shentsize={e_shentsize}, shnum={e_shnum}, shstrndx={e_shstrndx}")
    
    # Read string table
    f.seek(e_shoff + e_shstrndx * e_shentsize)
    shstr = f.read(e_shentsize)
    shstr_off, shstr_size = struct.unpack('<II', shstr[16:24])
    f.seek(shstr_off)
    names = f.read(shstr_size)
    
    f.seek(e_shoff)
    for i in range(e_shnum):
        sh = f.read(e_shentsize)
        sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size = struct.unpack('<IIIIII', sh[:24])
        name = names[sh_name:].split(b'\x00')[0].decode('latin1')
        print(f"[{i:2d}] {name:<20} addr={hex(sh_addr)} off={hex(sh_offset)} size={hex(sh_size)}")

