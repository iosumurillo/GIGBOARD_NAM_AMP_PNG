with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct

# The hash in evil at 0x298e8d8 + 2 is 0x09f64ae7!
# Let's search for 0x09f64ae7 in evil:
p = 0
while True:
    pos = evil.find(struct.pack('>I', 0x09f64ae7), p)
    if pos == -1: break
    print(f'Found hash 0x09f64ae7 at 0x{pos:x}')
    p = pos + 1

