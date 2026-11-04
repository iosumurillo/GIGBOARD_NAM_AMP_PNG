with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

for m in re.finditer(rb'CurrentBlock|CurrentModule', data):
    print(f"Match at 0x{m.start():x}: {m.group()}")
    start = max(0, m.start() - 100)
    end = min(len(data), m.end() + 200)
    res = []
    for b in data[start:end]:
        if 32 <= b <= 126 or b in (10, 13, 9):
            res.append(chr(b))
        else:
            res.append('.')
    print(" ", "".join(res))

