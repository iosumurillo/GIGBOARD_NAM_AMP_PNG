with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = 0x298e8ef
start = max(0, pos - 50)
end = min(len(data), pos + 200)
chunk = data[start:end]

res = []
for b in chunk:
    if 32 <= b <= 126:
        res.append(chr(b))
    else:
        res.append(f"\\x{b:02x}")
print("".join(res))

