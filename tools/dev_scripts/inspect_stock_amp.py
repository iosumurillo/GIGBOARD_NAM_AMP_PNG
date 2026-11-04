from PIL import Image

im = Image.open('scratch/extracted_pngs/img_295_0x024e4d4f.png')
print('Stock amp img_295:', im.size, im.format, im.mode)
# Check corners / alpha:
print('Stock amp mode:', im.mode)
if 'A' in im.mode:
    print('Alpha min/max:', im.getextrema()[-1])

