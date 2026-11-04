import glob
import struct

files = sorted(glob.glob("/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/img_*.png"))
for p in files[:35]:
    with open(p, "rb") as f:
        data = f.read(24)
        w, h = struct.unpack(">II", data[16:24])
        print(f"{p.split('/')[-1]}: {w}x{h}")
