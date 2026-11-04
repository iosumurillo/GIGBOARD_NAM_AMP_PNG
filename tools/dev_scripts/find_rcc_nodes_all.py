import struct, re

with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

nodes = []
ts = b'\x00\x00\x01\x88\x95\x9d\x19\xe8'
for m in re.finditer(re.escape(ts), evil[0x298f000:0x2996000]):
    p = 0x298f000 + m.start() - 14
    name_off, flags, c1, c2, ts_val = struct.unpack('>IHIIQ', evil[p:p+22])
    nodes.append((p, name_off, flags, c1, c2))

name_base = 0x2987c58
def get_name(off):
    p = name_base + off
    if p + 6 >= len(evil): return '???'
    l = int.from_bytes(evil[p:p+2], 'big')
    if l > 100: return '???'
    return evil[p+6:p+6+l*2].decode('utf-16-be', errors='replace')

for p, name_off, flags, c1, c2 in nodes:
    name = get_name(name_off)
    if any(k in name for k in ['82', 'Lead', '800', 'Amp', 'Anxiety']):
        print(f'0x{p:x}: name="{name}", flags=0x{flags:x}, c1=0x{c1:x}, c2=0x{c2:x}')
