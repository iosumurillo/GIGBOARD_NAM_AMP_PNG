with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = 0x156840f
start = max(0, pos - 50)
end = min(len(data), pos + 300)
chunk = data[start:end]

s = ""
for b in chunk:
    if 32 <= b <= 126:
        s += chr(b)
    elif b == 0:
        if len(s) > 1:
            print(" ", s)
        s = ""

