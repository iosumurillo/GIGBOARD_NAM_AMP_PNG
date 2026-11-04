with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

start = 0x1a30e30
# Print until next file header (which is usually null bytes or import)
print(data[start:start+3000].decode('latin1', errors='ignore'))

