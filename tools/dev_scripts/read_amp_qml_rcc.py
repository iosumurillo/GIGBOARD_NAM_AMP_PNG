with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

# Let's see what is around 0x2d0f7f9
pos = 0x2d0f7f9
print(data[pos-50:pos+300])

