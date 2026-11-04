from PIL import Image

im = Image.open('/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/img_234_0x02180c1a.png').convert('L')
print(f"img_234: {im.width}x{im.height}")
for y in range(160, 320, 5):
    line = ""
    for x in range(20, im.width - 20, 3):
        v = im.getpixel((x, y))
        line += " " if v > 140 else "#"
    print(f"{y:3d}: {line}")

