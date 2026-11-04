with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re
matches = [m.start() for m in re.finditer(b'BlockDetailsSubPage', data[0x1a20000:0x1a35000])]
for m in matches:
    abs_pos = 0x1a20000 + m
    # Look back to find filename header
    hdr = data[max(0, abs_pos-80):abs_pos]
    print(f'At {hex(abs_pos)}: {hdr[-50:]}')

