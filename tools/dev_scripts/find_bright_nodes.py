import struct

with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

name_base = 0x2987c58
import re
ts_matches = [m.start() for m in re.finditer(b'\x00\x00\x01\x88\x95\x9d\x19\xe8', data[0x298f000:0x2996000])]
for m in ts_matches:
    node_offset = 0x298f000 + m - 14
    name_off, flags, c1, c2, ts = struct.unpack('>IHIIQ', data[node_offset:node_offset+22])
    if name_off in (0x6c86, 0x68c0):
        print(f'Node at 0x{node_offset:x}: name_off=0x{name_off:x} flags=0x{flags:x} c1=0x{c1:x} c2=0x{c2:x}')

