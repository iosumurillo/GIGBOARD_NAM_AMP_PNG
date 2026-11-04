with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

p = 0x298e8de
print('Bytes around 0x298e8de:')
print(data[p-10:p+50])
l = int.from_bytes(data[p:p+2], 'big')
h = int.from_bytes(data[p+2:p+6], 'big')
s = data[p+6:p+6+l*2].decode('utf-16-be', errors='replace')
print(f'l={l}, h=0x{h:x}, s="{s}"')

