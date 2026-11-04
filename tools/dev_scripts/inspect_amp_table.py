with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = 0x1560ed8
# Let's inspect 0x1560000 to 0x1561300
chunk = data[0x1560b00:0x1561200]
print("All strings in this table:")
for s in chunk.split(b'\x00'):
    if s:
        print(repr(s))

