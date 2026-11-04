with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = data.find(b'"children":{"Amp":')
chunk = data[pos:pos+3000].decode('latin1', errors='replace')
print(chunk)

