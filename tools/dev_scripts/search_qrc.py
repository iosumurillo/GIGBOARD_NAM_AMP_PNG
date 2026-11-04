with open(r'c:\Antigravity\HEADRUSH\scratch\Evil_gigboard', 'rb') as f:
    data = f.read()

import re

for m in re.finditer(b'anxiety', data, re.IGNORECASE):
    s = data[max(0, m.start()-40) : min(len(data), m.end()+60)]
    print(hex(m.start()), s)

