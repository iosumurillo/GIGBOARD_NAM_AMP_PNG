import struct
d = open('scratch/Evil_gigboard', 'rb').read()


def qhash(s):
    h = 0
    for ch in s:
        h = ((h << 4) + ord(ch)) & 0xffffffff
        h ^= (h & 0xf0000000) >> 23
        h &= 0x0fffffff
    return h


targets = {0x298e8d8: '82 LEAD 800 Bright.png', 0x298e512: '82 LEAD 800 Bright2.png'}
tgt = min(targets)
base = None
for b in range(tgt - 0x6000, tgt):
    p = b
    ok = 0
    while p < tgt and ok < 4000:
        l = struct.unpack('>H', d[p:p + 2])[0]
        if l == 0 or l > 200:
            break
        try:
            nm = d[p + 6:p + 6 + 2 * l].decode('utf-16-be')
        except Exception:
            break
        if struct.unpack('>I', d[p + 2:p + 6])[0] != qhash(nm):
            break
        p += 6 + 2 * l
        ok += 1
    if p == tgt and ok > 5:
        base = b
        print('base', hex(b), ok)
        break
print(base)
if base is not None:
    for off, name in targets.items():
        rel = off - base
        pat = struct.pack('>I', rel)
        i = 0
        while True:
            i = d.find(pat, i)
            if i < 0:
                break
            print(name, 'ref at', hex(i), d[i:i + 22].hex())
            i += 1

