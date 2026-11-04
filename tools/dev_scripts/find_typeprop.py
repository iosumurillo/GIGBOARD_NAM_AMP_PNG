with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

idx = 0
while True:
    pos = data.find(b'typeProp', idx)
    if pos == -1:
        break
    print(f"Found typeProp at 0x{pos:x}:")
    start = max(0, pos - 100)
    end = min(len(data), pos + 150)
    print(" ", repr(data[start:end]))
    idx = pos + 8

