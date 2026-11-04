import re
p = r'C:/Users/iosum/.gemini/antigravity/brain/47acffb5-1b93-4f9a-be37-e545b83d88e3/.user_uploaded/media_1793635573821_3f05626e.txt'
seen = {}
for l in open(p, errors='ignore').read().splitlines():
    m = re.match(r'\[\s*([\d.]+)s\] \+0x([0-9a-f]+) = 0x([0-9a-f]+)\s+f=(\S+)', l)
    if not m:
        continue
    ts, off, raw, f = m.groups()
    off = int(off, 16)
    if float(ts) > 1:
        e = seen.setdefault(off, [ts, ts, 0, f, f])
        e[1] = ts
        e[2] += 1
        e[4] = f
for off in sorted(seen):
    print(hex(off), 'first', seen[off][0], 'last', seen[off][1], 'changes', seen[off][2], 'final', seen[off][4])

