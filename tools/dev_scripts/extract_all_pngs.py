import os

with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

png_header = b'\x89PNG\r\n\x1a\n'
iend = b'IEND\xaeB`\x82'

out_dir = 'scratch/extracted_pngs'
os.makedirs(out_dir, exist_ok=True)

pos = 0
count = 0
while True:
    p = data.find(png_header, pos)
    if p == -1:
        break
    end = data.find(iend, p)
    if end != -1:
        end += len(iend)
        png_data = data[p:end]
        count += 1
        out_file = os.path.join(out_dir, f'img_{count:03d}_0x{p:08x}.png')
        with open(out_file, 'wb') as out_f:
            out_f.write(png_data)
        pos = end
    else:
        pos = p + 8

print(f"Successfully extracted {count} PNG images to {out_dir}")
