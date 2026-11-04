with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import struct
for off in [0x24e4d4f, 0x23e329d]:
    prefix = evil[off-8:off]
    length = int.from_bytes(evil[off-4:off], 'big')
    print(f'Offset 0x{off:x}: prefix={prefix.hex()}, length={length} (0x{length:x})')

