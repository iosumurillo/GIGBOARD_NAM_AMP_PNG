with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

start = data.find(b'property string propertyPath: "/Engine/Patch/Amp"')
print(data[start:start+4000].decode('latin1', errors='ignore'))

