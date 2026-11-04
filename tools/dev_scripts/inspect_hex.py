with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = 0x1837d7d
chunk = data[pos-60:pos+10]
for i in range(0, len(chunk), 16):
    hex_str = " ".join(f"{b:02x}" for b in chunk[i:i+16])
    ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk[i:i+16])
    print(f"0x{pos-60+i:x}: {hex_str.ljust(48)} {ascii_str}")

