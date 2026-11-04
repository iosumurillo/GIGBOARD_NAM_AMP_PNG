with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = 0x15e2764
chunk = data[pos-600:pos+1000]
import re
print("Strings in this region:")
for s in re.findall(rb'[A-Za-z0-9_]{2,}', chunk):
    print(s.decode('latin1'))

