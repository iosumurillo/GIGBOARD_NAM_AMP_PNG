with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

# Let's inspect bytes near 0x298e8da
needle = '82 LEAD 800 Bright.png'.encode('utf-16-be')
pos = evil.find(needle)
print('needle pos:', hex(pos))
if pos != -1:
    hdr_pos = pos - 6
    l = int.from_bytes(evil[hdr_pos:hdr_pos+2], 'big')
    h = int.from_bytes(evil[hdr_pos+2:hdr_pos+6], 'big')
    print(f'hdr_pos=0x{hdr_pos:x}, l={l}, h=0x{h:08x}')

needle2 = '82 LEAD 800 Bright2.png'.encode('utf-16-be')
pos2 = evil.find(needle2)
print('needle2 pos:', hex(pos2))
if pos2 != -1:
    hdr_pos2 = pos2 - 6
    l2 = int.from_bytes(evil[hdr_pos2:hdr_pos2+2], 'big')
    h2 = int.from_bytes(evil[hdr_pos2+2:hdr_pos2+6], 'big')
    print(f'hdr_pos2=0x{hdr_pos2:x}, l2={l2}, h2=0x{h2:08x}')

