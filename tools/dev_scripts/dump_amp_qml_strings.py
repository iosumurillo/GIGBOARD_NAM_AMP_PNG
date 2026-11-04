with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    f.seek(0x2d0c570)
    data = f.read(0x2d0f7f8 - 0x2d0c570 + 200)

import re

# Find all UTF-16LE strings (consecutive characters where high byte is 0x00)
pos = 0
while pos < len(data) - 4:
    if data[pos+1] == 0 and 32 <= data[pos] < 127:
        start = pos
        s = []
        while pos < len(data) - 1 and data[pos+1] == 0 and 32 <= data[pos] < 127:
            s.append(chr(data[pos]))
            pos += 2
        st = ''.join(s)
        if len(st) >= 2:
            print(f"0x{0x2d0c570 + start:x}: {st}")
    else:
        pos += 1

