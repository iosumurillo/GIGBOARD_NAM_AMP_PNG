with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

for m in re.finditer(rb'ModuleEditors/Amp\.qml|Amp\.qml', data):
    print(f"0x{m.start():x}: {m.group()}")
    start = max(0, m.start() - 50)
    end = min(len(data), m.end() + 200)
    print(" ", repr(data[start:end]))

