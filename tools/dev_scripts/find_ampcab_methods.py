with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

# Search for AmpCab method symbols or strings
for m in re.finditer(rb'AmpCab[A-Za-z0-9_:]*', data):
    print(hex(m.start()), m.group().decode('latin1'))

