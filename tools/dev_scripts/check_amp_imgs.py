with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

# Let's inspect what image is at 0x24e4d4f
p1 = 0x24e4d4f
p2 = 0x23e329d

print(f'At 0x{p1:x}: header={evil[p1:p1+16]}')
print(f'At 0x{p2:x}: header={evil[p2:p2+16]}')

# In extract_all_pngs, which image was at 0x24e4d4f?
# Let's check scratch/extracted_pngs
import glob
f1 = glob.glob(f'scratch/extracted_pngs/*0x{p1:08x}.png')
f2 = glob.glob(f'scratch/extracted_pngs/*0x{p2:08x}.png')
print('File 1:', f1)
print('File 2:', f2)

