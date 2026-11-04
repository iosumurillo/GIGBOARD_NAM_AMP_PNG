with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

start = 0x2980000
end = 0x298e100
chunk = data[start:end]

import re
matches = []
for m in re.finditer(rb'(\x00[\x20-\x7e]){2,}', chunk):
    s = m.group().decode('utf-16-be', errors='replace')
    if '/' in s or 'img' in s or 'Pages' in s or 'Images' in s:
        matches.append((start + m.start(), s))

for addr, s in matches[-20:]:
    print(f"0x{addr:x}: {s}")

