with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

start = 0x1837d1e
length = 0x1a3
qml = data[start:start+length]
print(f"Length: {len(qml)} bytes")
print(qml.decode('utf-8'))

