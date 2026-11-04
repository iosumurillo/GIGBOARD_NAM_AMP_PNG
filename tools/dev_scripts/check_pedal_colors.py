import glob
from PIL import Image

files = sorted(glob.glob("/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/img_*.png"))
pedals = []
for p in files:
    try:
        im = Image.open(p)
        w, h = im.size
        if (280 <= w <= 320 and 420 <= h <= 460) or (220 <= w <= 240 and 390 <= h <= 420):
            # calculate average color
            im_rgb = im.convert('RGB')
            pixels = list(im_rgb.getdata())
            # sample every 10 pixels
            pixels_sample = pixels[::10]
            avg_r = sum(px[0] for px in pixels_sample) // len(pixels_sample)
            avg_g = sum(px[1] for px in pixels_sample) // len(pixels_sample)
            avg_b = sum(px[2] for px in pixels_sample) // len(pixels_sample)
            pedals.append((p.split('/')[-1], w, h, (avg_r, avg_g, avg_b)))
    except Exception as e:
        pass

print(f"Total pedal-sized images: {len(pedals)}")
for name, w, h, rgb in pedals:
    print(f"{name}: {w}x{h}, avg RGB: {rgb}")

