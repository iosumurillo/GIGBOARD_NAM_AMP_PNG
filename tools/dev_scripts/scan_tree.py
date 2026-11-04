import struct, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

name_base = 0x2987c58

def get_name(off):
    p = name_base + off
    if p + 6 >= len(data): return "???"
    length = int.from_bytes(data[p:p+2], 'big')
    if length > 200: return "???"
    chars = data[p+6:p+6+length*2].decode('utf-16-be', errors='replace')
    return chars

# Search for all occurrences of the timestamp:
import re
ts_matches = [m.start() for m in re.finditer(b'\x00\x00\x01\x88\x95\x9d\x19\xe8', data[0x298f000:0x2996000])]
print(f'Total timestamp matches: {len(ts_matches)}')

# Each match is at offset +14 of a 22-byte node
nodes = []
for m in ts_matches:
    node_offset = 0x298f000 + m - 14
    name_off, flags, c1, c2, ts = struct.unpack('>IHIIQ', data[node_offset:node_offset+22])
    name = get_name(name_off)
    is_dir = (flags & 2) != 0
    nodes.append((node_offset, name_off, name, is_dir, c1, c2))

print(f'Parsed {len(nodes)} nodes.')
png_nodes = [n for n in nodes if not n[3] and n[2].endswith('.png')]
print(f'Total PNG file nodes: {len(png_nodes)}')

for n in png_nodes:
    if any(k in n[2].upper() for k in ['ANXIETY', 'OCT', 'M-GEAR', 'FUZZ', '82 LEAD']):
        print(f'Node at 0x{n[0]:x}: name="{n[2]}" data_offset=0x{n[5]:x}')


