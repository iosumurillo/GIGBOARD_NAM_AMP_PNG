import re
p = r'C:/Users/iosum/.gemini/antigravity/brain/47acffb5-1b93-4f9a-be37-e545b83d88e3/.user_uploaded/media_1793635573821_3f05626e.txt'
n = 0
for l in open(p, errors='ignore').read().splitlines():
    m = re.match(r'\[\s*([\d.]+)s\] \+0x([0-9a-f]+) = 0x([0-9a-f]+)\s+f=(\S+)', l)
    if not m:
        if 'PROCESS' in l:
            print(l)
        continue
    ts, off, raw, f = m.groups()
    off = int(off, 16)
    if (0x9500 <= off <= 0x953c or off in (0x95a4, 0x95a8, 0x268, 0x26c)) and float(ts) > 1:
        print(ts, hex(off), raw, f)
        n += 1
        if n > 150:
            break

