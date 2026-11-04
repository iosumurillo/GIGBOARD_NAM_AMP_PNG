import os

os.makedirs('scratch/pedals', exist_ok=True)
with open(r'c:\Antigravity\HEADRUSH\scratch\Evil_gigboard', 'rb') as f:
    data = f.read()

png_magic = b'\x89PNG\r\n\x1a\n'
pos = 0
idx_count = 0
while True:
    idx = data.find(png_magic, pos)
    if idx == -1: break
    iend = data.find(b'IEND', idx)
    if iend != -1:
        plen = (iend + 8) - idx
        w = int.from_bytes(data[idx+16:idx+20], 'big')
        h = int.from_bytes(data[idx+20:idx+24], 'big')
        if (w, h) in [(286, 442), (286, 436)]:
            idx_count += 1
            filename = f'scratch/pedals/pedal_{idx_count:02d}_{hex(idx)}_{w}x{h}_{plen}.png'
            with open(filename, 'wb') as pf:
                pf.write(data[idx:idx+plen])
            print(f'Wrote {filename}')
        pos = iend + 8
    else:
        pos = idx + 8

