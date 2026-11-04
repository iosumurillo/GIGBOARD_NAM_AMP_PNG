import lzma

with open('scratch/Update_patched.img', 'rb') as f:
    fit_data = f.read()

decomp = lzma.decompress(fit_data[1298064:])

# Find the PNG in decomp
# Look for 'IHDR'
png_magic = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
pos = 0
found = []
while True:
    idx = decomp.find(png_magic, pos)
    if idx == -1: break
    # Find IEND
    iend = decomp.find(b'IEND\xaeB`\x82', idx)
    if iend != -1:
        png_len = (iend + 8) - idx
        found.append((idx, png_len))
        pos = iend + 8
    else:
        pos = idx + 1

print(f'Found {len(found)} PNGs in rootfs')
# Let's see which ones correspond to Anxiety OD
for idx, plen in found:
    if plen in [75435, 63031]:
        print(f'Found candidate PNG at {hex(idx)}, len={plen}')
        with open(f'scratch/extracted_{plen}.png', 'wb') as pf:
            pf.write(decomp[idx:idx+plen])

