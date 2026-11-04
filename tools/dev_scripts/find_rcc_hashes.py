with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct

# In Qt RCC, name_off can be relative to names_base:
# What if names_base is NOT 0x2987c58 for images?
# What if there are MULTIPLE RCC resources?
# Let's search for "qInitResources" or check how many RCC trees exist.
# In Qt, resource data starts with magic or has a known structure.
# Let's search for the hash of 'Anxiety OD.png' or '82 LEAD 800 Bright.png'!

# Qt hash function:
def qt_hash(s):
    h = 0
    for c in s:
        h = ((h << 4) + ord(c)) & 0xffffffff
        g = h & 0xf0000000
        if g != 0:
            h ^= (g >> 24)
        h &= ~g
    return h

h_anx = qt_hash('Anxiety OD.png')
h_lead = qt_hash('82 LEAD 800 Bright.png')
print(f'Hash Anxiety: 0x{h_anx:08x}')
print(f'Hash Lead: 0x{h_lead:08x}')

# Let's search for these hashes in evil:
p = 0
while True:
    pos = evil.find(struct.pack('>I', h_lead), p)
    if pos == -1: break
    print(f'Found Lead hash (BE) at 0x{pos:x}')
    print(evil[pos-10:pos+30].hex())
    p = pos + 1

