with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

# Search for QML filenames in Evil
for m in re.finditer(rb'([a-zA-Z0-9_/\\-]+\.qml)', data):
    name = m.group()
    if b'Amp' in name or b'amp' in name or b'Pedal' in name or b'pedal' in name or b'Module' in name or b'Chain' in name or b'Block' in name:
        print(f"0x{m.start():x}: {name.decode('utf-8', errors='replace')}")

