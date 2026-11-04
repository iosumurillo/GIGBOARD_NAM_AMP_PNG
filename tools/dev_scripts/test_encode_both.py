import io
import struct
import zlib
from PIL import Image, ImageDraw

SRC_AMP = r'C:/Users/iosum/.gemini/antigravity/brain/47acffb5-1b93-4f9a-be37-e545b83d88e3/.user_uploaded/media_1793778228977_4abc4965.jpg'
SRC_PEDAL = r'C:/Users/iosum/.gemini/antigravity/brain/47acffb5-1b93-4f9a-be37-e545b83d88e3/.user_uploaded/media_1793778228916_c38d5f47.jpg'

evil = open('scratch/Evil_gigboard', 'rb').read()

def cutout_pedal():
    im = Image.open(SRC_PEDAL).convert('RGBA')
    w, h = im.size
    # Key out the white corners
    for pt in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        ImageDraw.floodfill(im, pt, (255, 255, 255, 0), thresh=28)
    return im

def cutout_amp():
    im = Image.open(SRC_AMP).convert('RGBA')
    # Let's inspect if the amp has any white corners or transparent parts:
    # Corner pixels in inspect_new_images:
    # [(180, 166, 157), (46, 35, 33), (63, 45, 41), (48, 33, 26)]
    # All are part of the wood frame / chassis!
    return im

def fit(im, W, H):
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    s = min(W / im.width, H / im.height)
    nw, nh = max(1, round(im.width * s)), max(1, round(im.height * s))
    im = im.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    canvas.paste(im, ((W - nw) // 2, (H - nh) // 2), im)
    return canvas

def encode(img, limit):
    last = None
    for colors in (256, 192, 128, 96, 64, 48, 32):
        q = img.quantize(colors=colors, method=Image.FASTOCTREE, dither=Image.NONE)
        buf = io.BytesIO()
        q.save(buf, 'PNG', optimize=True)
        data = buf.getvalue()
        last = (colors, len(data))
        if len(data) <= limit - 12:
            return data
    raise SystemExit('cannot fit in %d: %s' % (limit, last))

def pad(png, target):
    iend = png.rfind(b'IEND') - 4
    head, tail = png[:iend], png[iend:]
    diff = target - len(png)
    assert diff >= 12, diff
    ct = b'paDd'
    payload = b'\x00' * (diff - 12)
    crc = zlib.crc32(ct + payload) & 0xffffffff
    out = head + struct.pack('>I', len(payload)) + ct + payload + struct.pack('>I', crc) + tail
    assert len(out) == target
    Image.open(io.BytesIO(out)).load()
    return out

pedal_base = cutout_pedal()
amp_base = cutout_amp()

ANX_LEN = 75435
anx = pad(encode(fit(pedal_base, 286, 442), ANX_LEN), ANX_LEN)
open('scratch/user_anxiety.png', 'wb').write(anx)
print('Pedal PNG encoded successfully! Size:', len(anx))

AMP_A_LEN = 60104
amp_a = pad(encode(fit(amp_base, 290, 119), AMP_A_LEN), AMP_A_LEN)
open('scratch/user_AMP_A.png', 'wb').write(amp_a)
print('Amp A PNG encoded successfully! Size:', len(amp_a))

AMP_B_LEN = 61391
amp_b = pad(encode(fit(amp_base, 290, 119), AMP_B_LEN), AMP_B_LEN)
open('scratch/user_AMP_B.png', 'wb').write(amp_b)
print('Amp B PNG encoded successfully! Size:', len(amp_b))

