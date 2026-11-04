with open(r'c:\Antigravity\HEADRUSH\scratch\Evil_gigboard', 'rb') as f:
    data = f.read()

png_magic = b'\x89PNG\r\n\x1a\n'
pos = 0
found = []
while True:
    idx = data.find(png_magic, pos)
    if idx == -1: break
    iend = data.find(b'IEND', idx)
    if iend != -1:
        plen = (iend + 8) - idx
        w = int.from_bytes(data[idx+16:idx+20], 'big')
        h = int.from_bytes(data[idx+20:idx+24], 'big')
        if (w, h) in [(286, 442), (286, 436)]:
            found.append((idx, plen, w, h))
        pos = iend + 8
    else:
        pos = idx + 8

print(f'Found {len(found)} candidate pedal PNGs:')
for idx, plen, w, h in found:
    print(f'Offset {hex(idx)}: {w}x{h}, len={plen}')

