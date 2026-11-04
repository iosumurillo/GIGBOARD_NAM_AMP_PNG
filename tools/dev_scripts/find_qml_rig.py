with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

for m in re.finditer(rb'import QtQuick', data[0x1800000:0x1850000]):
    start = 0x1800000 + m.start()
    end = data.find(b'\x00\x00', start)
    if end == -1 or end - start > 10000:
        end = start + 2000
    qml_text = data[start:end]
    print(f"--- QML at 0x{start:x} (len {len(qml_text)}) ---")
    print(qml_text.decode('utf-8', errors='replace')[:400])

