with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

start = 0x1564c00
end = 0x1565200
chunk = data[start:end]

s = ""
items = []
for b in chunk:
    if b == 0:
        if len(s) > 0:
            items.append(s)
            s = ""
    elif 32 <= b <= 126:
        s += chr(b)
    else:
        s = ""

for i, a in enumerate(items):
    print(f"[{i}] {a}")

