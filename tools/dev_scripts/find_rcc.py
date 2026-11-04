with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

# Search for Qt resource name prefixes
pos = 0
while True:
    pos = data.find(b'LEAD 800', pos)
    if pos == -1:
        break
    print(f"Match at 0x{pos:x}:")
    print("  ", repr(data[pos-32:pos+48]))
    pos += 8

