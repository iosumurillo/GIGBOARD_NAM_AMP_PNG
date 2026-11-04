with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

for m in re.finditer(rb'GainA', data):
    start = max(0, m.start() - 30)
    end = min(len(data), m.end() + 50)
    print(hex(m.start()), repr(data[start:end]))

