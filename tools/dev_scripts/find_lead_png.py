with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

# Look for anything like "LEAD" or "Lead" near "png" or ".png"
for m in re.finditer(rb'Lead[^\x00\r\n]{0,50}\.png|LEAD[^\x00\r\n]{0,50}\.png', data, re.IGNORECASE):
    print(f"Match at 0x{m.start():x}: {m.group()}")

# Also look for where "qrc:" appears with images
for m in re.finditer(rb'qrc:/[^\x00\r\n\t "]{3,60}\.png', data):
    print(f"qrc png match at 0x{m.start():x}: {m.group()}")

