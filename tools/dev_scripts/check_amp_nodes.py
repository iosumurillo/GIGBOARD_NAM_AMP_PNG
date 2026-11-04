import struct, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

name_base = 0x2987c58

def get_name(off):
    p = name_base + off
    if p + 6 >= len(data): return '???'
    length = int.from_bytes(data[p:p+2], 'big')
    if length > 200: return '???'
    chars = data[p+6:p+6+length*2].decode('utf-16-be', errors='replace')
    return chars

import re
ts_matches = [m.start() for m in re.finditer(b'\x00\x00\x01\x88\x95\x9d\x19\xe8', data[0x298f000:0x2996000])]
for m in ts_matches:
    node_offset = 0x298f000 + m - 14
    name_off, flags, c1, c2, ts = struct.unpack('>IHIIQ', data[node_offset:node_offset+22])
    name = get_name(name_off)
    if any(k in name.lower() for k in ['82', 'lead', '800', 'amp']):
        print(f'Node at 0x{node_offset:x}: name="{name}" is_dir={bool(flags&2)} c1=0x{c1:x} c2=0x{c2:x}')

