import struct
from PIL import Image
import io
d = open('scratch/Evil_gigboard', 'rb').read()
SIG = b'\x89PNG\r\n\x1a\n'
offs = {'Bright.png': 0x24a963, 'Bright2a': 0x148eb1, 'Bright2b': 0x25784}
pos = []
i = 0
while True:
    i = d.find(SIG, i)
    if i < 0:
        break
    pos.append(i)
    i += 1
posset = set(pos)
cands = [p - 4 - 0x24a963 for p in pos]
for b in cands:
    hits = [n for n, o in offs.items() if (b + o + 4) in posset]
    if len(hits) >= 2:
        print('base', hex(b), hits)
        for n, o in offs.items():
            a = b + o
            ln = struct.unpack('>I', d[a:a + 4])[0]
            png = d[a + 4:a + 4 + ln]
            try:
                im = Image.open(io.BytesIO(png))
                print(n, hex(a + 4), ln, im.size, im.mode)
                open('scratch/amp_%s.png' % n, 'wb').write(png)
            except Exception as e:
                print(n, 'err', e)

