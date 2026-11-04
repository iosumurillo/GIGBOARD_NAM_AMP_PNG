with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

# Let's inspect 0x298e8da
p = 0x298e8da
l = int.from_bytes(evil[p:p+2], 'big')
h = int.from_bytes(evil[p+2:p+6], 'big')
raw_chars = evil[p+6:p+6+l*2]
s = raw_chars.decode('utf-16-be')
print(f'At 0x{p:x}: len={l}, hash=0x{h:08x}, name="{s}"')

# And 0x298e518:
p2 = 0x298e518 - 4
l2 = int.from_bytes(evil[p2:p2+2], 'big')
h2 = int.from_bytes(evil[p2+2:p2+6], 'big')
raw_chars2 = evil[p2+6:p2+6+l2*2]
s2 = raw_chars2.decode('utf-16-be')
print(f'At 0x{p2:x}: len={l2}, hash=0x{h2:08x}, name="{s2}"')

