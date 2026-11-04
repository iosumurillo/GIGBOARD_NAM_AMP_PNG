with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

p = 0x2987c58
for i in range(10):
    l = int.from_bytes(data[p:p+2], 'big')
    h = int.from_bytes(data[p+2:p+6], 'big')
    s = data[p+6:p+6+l*2].decode('utf-16-be', errors='replace')
    print(f'p=0x{p:x}: len={l}, hash=0x{h:x}, name="{s}"')
    p += 6 + l * 2

