from PIL import Image

for name in ['img_234_0x02180c1a.png', 'img_235_0x02190255.png']:
    im = Image.open(f'/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/{name}')
    # Let's see what color the corners, center, and text areas are
    # In a pedal image, the top usually has knobs (y: 50-200), center has text/logo (y: 200-300), bottom has switch (y: 350-430)
    w, h = im.size
    print(f"\n--- {name} ({w}x{h}) ---")
    for y in range(0, h, 40):
        row = [im.getpixel((x, y)) for x in range(20, w-20, 30)]
        print(f"y={y:3d}: {[p[:3] for p in row]}")

