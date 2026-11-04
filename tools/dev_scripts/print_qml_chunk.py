with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

start = 0x1837d50
end = 0x1838000
chunk = data[start:end]
print(chunk.decode('utf-8', errors='replace'))

