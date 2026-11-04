with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

# In Qt RCC, names are UTF-16 BE with length prefix, e.g. \x00\x16 ...
# Let's see what directory tree encloses this name
pos = 0x298e8ef
start = pos - 2000
chunk = data[start:pos+500]

# find all UTF-16 strings in chunk
import re
# look for 2-byte char sequence where every 2nd byte is ascii
matches = []
for m in re.finditer(rb'(\x00[\x20-\x7e]){3,}', chunk):
    s = m.group().decode('utf-16-be', errors='replace')
    matches.append((start + m.start(), s))

for addr, s in matches:
    print(f"0x{addr:x}: {s}")

