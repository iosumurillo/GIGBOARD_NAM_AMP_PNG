with open('firmware_rootfs/usr/bin/Resources/StringTables.xml', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'<string[^>]*>.*?</string>', text, re.IGNORECASE)
print(f'Total strings in StringTables.xml: {len(matches)}')
for m in matches:
    if any(k in m.upper() for k in ['GAIN', 'MAST', 'BRIGHT', 'LEAD 800', 'TREMOLO']):
        print(' ', m)

