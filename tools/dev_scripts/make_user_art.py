import io
import struct
import zlib
from PIL import Image, ImageDraw

SRC = r'C:/Users/iosum/.gemini/antigravity/brain/47acffb5-1b93-4f9a-be37-e545b83d88e3/.user_uploaded/media_1793689161428_898e4d41.jpg'
evil = open('scratch/Evil_gigboard', 'rb').read()


def cutout():
    im = Image.open(SRC).convert('RGBA')
    w, h = im.size
    # key out the white studio background by flood fill from the 4 corners
    for pt in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1)]:
        ImageDraw.floodfill(im, pt, (255, 255, 255, 0), thresh=28)
    return im


def fit(im, W, H):
    bbox = im.getbbox()
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


def carray(name, data):
    s = 'static const uint8_t %s[%d] = {\n' % (name, len(data))
    for i in range(0, len(data), 16):
        s += '  ' + ','.join('0x%02x' % b for b in data[i:i + 16]) + ',\n'
    return s + '};\n\n'


base = cutout()

# Anxiety OD (stock PNG 286x442, 75435 bytes incl. both v1/v2 copies)
ANX_LEN = 75435
anx = pad(encode(fit(base, 286, 442), ANX_LEN), ANX_LEN)
open('scratch/user_anxiety.png', 'wb').write(anx)

# Amp 82 LEAD 800 Bright (290x119 slot)
amps = [('AMP_A', 0x24e4d4f, 60104), ('AMP_B', 0x23e329d, 61391)]
hdr = '/* Auto-generated user artwork patches */\n#ifndef USER_ART_PATCH_H\n#define USER_ART_PATCH_H\n\n#include <stddef.h>\n#include <stdint.h>\n\n'
amp_out = []
for name, off, ln in amps:
    orig = evil[off:off + ln]
    assert orig[:8] == b'\x89PNG\r\n\x1a\n'
    needle = orig[:48]
    hdr += '#define %s_OFF 0x%xu\n' % (name, off)
    png = pad(encode(fit(base, 290, 119), ln), ln)
    open('scratch/user_%s.png' % name, 'wb').write(png)
    hdr += '#define %s_LEN %d\n' % (name, ln)
    hdr += carray('%s_NEEDLE' % name, needle).replace('[%d]' % len(needle), '[48]')
    hdr += carray('%s_PNG' % name, png)
hdr += '#endif\n'
open('core/user_art_patch.h', 'w').write(hdr)

# regenerate Anxiety header
a = '/* Auto-generated user pedal PNG patch (%d bytes) */\n#ifndef ANXIETY_OD_PNG_PATCH_H\n#define ANXIETY_OD_PNG_PATCH_H\n\n#include <stddef.h>\n#include <stdint.h>\n\n#define ANXIETY_OD_PNG_PATCH_LEN %d\n\n' % (ANX_LEN, ANX_LEN)
a += carray('ANXIETY_OD_PNG_PATCH', anx) + '#endif /* ANXIETY_OD_PNG_PATCH_H */\n'
open('core/anxiety_od_png_patch.h', 'w').write(a)
print('done', len(anx))
