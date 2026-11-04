import struct

with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

tree_base = 0x298f950
for i in range(305):
    p = tree_base + i * 22
    name_off, flags, c1, c2, ts = struct.unpack('>IHIIQ', data[p:p+22])
    if abs(name_off - 0x419a) < 0x20:
        print(f'Node {i}: name_off={hex(name_off)}, data_offset={hex(c2)}')
