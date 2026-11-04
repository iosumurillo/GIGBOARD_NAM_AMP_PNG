with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = 0x1572c19
start = max(0, pos - 200)
end = min(len(data), pos + 1000)
chunk = data[start:end]

s = ""
for b in chunk:
    if 32 <= b <= 126:
        s += chr(b)
    elif b == 0:
        if len(s) > 2:
            print(" ", s)
        s = ""

