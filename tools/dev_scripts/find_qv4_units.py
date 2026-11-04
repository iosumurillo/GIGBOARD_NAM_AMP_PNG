with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

matches = [m.start() for m in re.finditer(rb'qv4cdata', data)]
for m in matches:
    unit = data[m:m+8000]
    b_ascii = any(k in unit for k in [b'Bright', b'Bass', b'Presence', b'GainA', b'GainB'])
    b_utf16 = any(k.encode('utf-16le') in unit for k in ['Bright', 'Bass', 'Presence', 'GainA', 'GainB'])
    if b_ascii or b_utf16:
        print(f"Match at {hex(m)}: ascii={b_ascii}, utf16={b_utf16}")
