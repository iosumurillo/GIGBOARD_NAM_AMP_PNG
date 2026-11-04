with open('C:/Antigravity/HEADRUSH/scratch/decompressed_qml/qml_034_1861fd1.qml', 'rb') as f:
    data = f.read().decode('utf-8', errors='ignore')

import re
# Find anything about pages, swipe, dot, param
for line in data.splitlines():
    if any(k in line for k in ['param', 'page', 'swipe', 'Page', 'knob', 'Knob']):
        print(line.strip())

