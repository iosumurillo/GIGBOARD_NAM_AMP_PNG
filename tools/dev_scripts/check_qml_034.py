with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

# Let's check where qml_034 comes from
# In decompressed_qml: qml_034_1861fd1.qml
# 0x1861fd1 is the offset in Evil!
off = 0x1861fd1
print('Bytes around 0x1861fd1:', evil[off-4:off+30].hex())
l = int.from_bytes(evil[off-4:off], 'big')
print(f'Length at 0x{off:x}: {l} (0x{l:x})')

