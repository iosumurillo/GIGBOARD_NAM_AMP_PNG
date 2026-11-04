from PIL import Image

for name in ['img_234_0x02180c1a.png', 'img_235_0x02190255.png']:
    im = Image.open(f'/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/{name}').convert('L')
    print(f"\n==================== {name} ====================")
    # Check y from 180 to 320 (text region), downsampled by 4 in x and 8 in y
    for y in range(180, 320, 6):
        line = ""
        for x in range(30, im.width - 30, 4):
            val = im.getpixel((x, y))
            line += " " if val > 150 else ("#" if val < 80 else ".")
        if "#" in line or "." in line:
            print(f"{y:3d}: {line}")

