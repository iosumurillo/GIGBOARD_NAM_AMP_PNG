from PIL import Image

im = Image.open('scratch/extracted_pngs/img_295_0x024e4d4f.png')
print('Stock bbox:', im.getbbox())

