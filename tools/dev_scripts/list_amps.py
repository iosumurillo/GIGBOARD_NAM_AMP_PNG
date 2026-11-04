with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

start = 0x1560c00
end = 0x1561200
chunk = data[start:end]

s = ""
amps = []
for b in chunk:
    if b == 0:
        if len(s) > 0:
            amps.append(s)
            s = ""
    elif 32 <= b <= 126:
        s += chr(b)
    else:
        s = ""

for i, a in enumerate(amps):
    print(f"[{i}] {a}")

