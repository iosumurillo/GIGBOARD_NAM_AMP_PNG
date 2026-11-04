from PIL import Image

im = Image.open('/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/img_235_0x02190255.png')
print(f"img_235 size: {im.size}")
# Find all pixels that are not light grey
dark_pixels = []
for y in range(im.height):
    for x in range(im.width):
        r, g, b, a = im.getpixel((x, y))
        if a > 100 and (r < 150 or g < 150 or b < 150):
            dark_pixels.append((x, y, (r, g, b)))

print(f"Total dark pixels: {len(dark_pixels)}")
# find bounding box of dark pixels
if dark_pixels:
    min_x = min(p[0] for p in dark_pixels)
    max_x = max(p[0] for p in dark_pixels)
    min_y = min(p[1] for p in dark_pixels)
    max_y = max(p[1] for p in dark_pixels)
    print(f"Dark pixels bounding box: x={min_x}..{max_x}, y={min_y}..{max_y}")

