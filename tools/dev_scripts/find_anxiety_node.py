with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct
target = 0x298da92 - 0x2987c58
print('Searching for name_off =', hex(target))
p = 0
while True:
    pos = evil.find(struct.pack('>I', target), p)
    if pos == -1: break
    print(f'Found at 0x{pos:x}:', evil[pos:pos+22].hex())
    p = pos + 1

