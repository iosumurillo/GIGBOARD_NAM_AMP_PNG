with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re

# Look for image files associated with amps or pedals
# e.g. "Lead 800" or "LEAD 800" or ".png"
for m in re.finditer(rb'LEAD[ _\-]800[^\x00\r\n]{0,30}', data, re.IGNORECASE):
    print(f"Match at 0x{m.start():x}: {m.group()}")
    start = max(0, m.start() - 32)
    end = min(len(data), m.end() + 32)
    print("  context:", repr(data[start:end]))

