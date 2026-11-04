from PIL import Image

for name in ['img_234_0x02180c1a.png', 'img_235_0x02190255.png']:
    im = Image.open(f'/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/{name}')
    print(f"{name}: format={im.format}, size={im.size}, mode={im.mode}")

