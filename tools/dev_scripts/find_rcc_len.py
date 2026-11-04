with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import struct

# Qt5 RCC data table: each file entry has:
# 4 bytes length, followed by data.
# Let's search backwards from 0x1837d35 for 4-byte BE length that matches the file size!
# The file ends at 0x1837ec5 ('}\r\n\r\n')
# Let's check candidate lengths: 0x1837ec5 - start
for start in range(0x1837d00, 0x1837d36):
    file_len = 0x1837ec5 - start
    prefix = struct.pack('>I', file_len)
    if data[start-4:start] == prefix:
        print(f"MATCH! start=0x{start:x}, len={file_len}")
        break
    # or maybe little endian?
    prefix_le = struct.pack('<I', file_len)
    if data[start-4:start] == prefix_le:
        print(f"MATCH LE! start=0x{start:x}, len={file_len}")
        break
else:
    print("Direct length prefix not found, checking nearby length words...")
    for off in range(0x1837cb0, 0x1837d40, 4):
        be = struct.unpack('>I', data[off:off+4])[0]
        le = struct.unpack('<I', data[off:off+4])[0]
        print(f"0x{off:x}: BE=0x{be:x} ({be}), LE=0x{le:x} ({le})")

