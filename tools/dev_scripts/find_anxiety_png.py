import glob
from PIL import Image

# Let's inspect the candidate pedal images around img_160 to img_250
files = sorted(glob.glob("/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/img_*.png"))
for p in files:
    try:
        im = Image.open(p)
        w, h = im.size
        # Filter for typical pedal aspect ratio
        if (280 <= w <= 290 and 430 <= h <= 460):
            # Let's check text around y: 220 to 320
            crop = im.crop((20, 220, w-20, 320)).convert('L')
            # Check variance or darkest pixels
            darkest = min(crop.getdata())
            lightest = max(crop.getdata())
            # If contrast is high (text), print info
            contrast = lightest - darkest
            name = p.split('/')[-1]
            print(f"{name}: {w}x{h}, contrast in text area={contrast}, range={darkest}..{lightest}")
    except:
        pass

