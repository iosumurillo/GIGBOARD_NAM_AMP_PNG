with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

idx = 0
target = b'82 LEAD 800 Bright'
while True:
    pos = data.find(target, idx)
    if pos == -1:
        break
    print(f"Found '{target.decode()}' at 0x{pos:x}")
    start = max(0, pos - 80)
    end = min(len(data), pos + len(target) + 80)
    print("  Context:", repr(data[start:end]))
    idx = pos + len(target)

target2 = b'800 Bright'
while True:
    pos = data.find(target2, idx)
    if pos == -1:
        break
    print(f"Found '{target2.decode()}' at 0x{pos:x}")
    start = max(0, pos - 80)
    end = min(len(data), pos + len(target2) + 80)
    print("  Context:", repr(data[start:end]))
    idx = pos + len(target2)

