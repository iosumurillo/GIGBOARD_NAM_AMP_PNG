with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

start = 0x1560000
end = 0x1562000
chunk = data[start:end]
# Extract all null-terminated strings
strings = []
cur = []
for i, b in enumerate(chunk):
    if b >= 32 and b <= 126:
        cur.append(chr(b))
    else:
        if len(cur) >= 4:
            strings.append((start + i - len(cur), "".join(cur)))
        cur = []

for addr, s in strings:
    if any(k in s for k in ['800', 'LEAD', 'Lead', 'JCM', 'Marshall', 'Bright', 'Amp', 'amp', 'Plexi']):
        print(f"0x{addr:x}: {s}")

