with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

for m in re.finditer(rb'BlockDetails\.qml', data):
    print(f"Match at 0x{m.start():x}")

# Let's search for "qrc:/Pages/BlockDetails.qml" or similar
for m in re.finditer(rb'qrc:/[^\x00\r\n\t "]{3,60}BlockDetails\.qml', data):
    print(f"qrc match at 0x{m.start():x}: {m.group()}")

