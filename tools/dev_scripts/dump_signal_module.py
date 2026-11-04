with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = 0x18494a8
start = max(0, pos - 100)
end = min(len(data), pos + 1500)
chunk = data[start:end]

res = []
for b in chunk:
    if 32 <= b <= 126 or b in (10, 13, 9):
        res.append(chr(b))
    else:
        res.append('.')

print("".join(res))

