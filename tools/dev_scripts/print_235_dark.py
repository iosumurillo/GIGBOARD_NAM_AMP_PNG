from PIL import Image

im = Image.open('/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/img_235_0x02190255.png')
for y in range(40, 420, 8):
    line = ""
    for x in range(30, 260, 4):
        r, g, b, a = im.getpixel((x, y))
        if a > 100 and (r < 170 or g < 170 or b < 170):
            line += "#"
        else:
            line += " "
    if "#" in line:
        print(f"{y:3d}: {line}")

