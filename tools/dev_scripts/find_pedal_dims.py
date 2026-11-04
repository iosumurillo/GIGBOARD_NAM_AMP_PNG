import glob
import struct

files = sorted(glob.glob("/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/img_*.png"))
print(f"Total files: {len(files)}")
for p in files:
    with open(p, "rb") as f:
        data = f.read(24)
        if len(data) >= 24 and data.startswith(b'\x89PNG\r\n\x1a\n'):
            w, h = struct.unpack(">II", data[16:24])
            if (200 <= w <= 400 and 300 <= h <= 600) or (100 <= w <= 200 and 150 <= h <= 300):
                print(f"{p.split('/')[-1]}: {w}x{h}")
