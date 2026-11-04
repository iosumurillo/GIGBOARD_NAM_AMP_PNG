import struct

with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

vaddr = 0x1560ed8 + 0x8000
needle = struct.pack('<I', vaddr)

idx = 0
while True:
    pos = data.find(needle, idx)
    if pos == -1:
        break
    print(f"Found pointer to string at 0x{pos:x} (vaddr 0x{pos+0x8000:x})")
    # inspect surrounding struct
    start = max(0, pos - 32)
    end = min(len(data), pos + 64)
    print("  Surrounding bytes:")
    for i in range(start, end, 4):
        val = struct.unpack('<I', data[i:i+4])[0]
        print(f"    0x{i+0x8000:x}: 0x{val:08x}")
    idx = pos + 4

