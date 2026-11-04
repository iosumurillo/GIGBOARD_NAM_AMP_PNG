with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = 0x1837d60 # approx start of this qml
# Search in data for references to this offset or (offset + 0x8000)
import struct

vaddr = pos + 0x8000
print(f"File offset: 0x{pos:x}, vaddr: 0x{vaddr:x}")

# In RCC (Qt5), qrc data table has 4-byte length (big endian) followed by data!
# Let's check 4 bytes before "import QtQuick 2.2" at 0x1837d7d
start_qml = 0x1837d63
len_be = struct.unpack('>I', data[start_qml-4:start_qml])[0]
print(f"BE Length prefix before QML at 0x{start_qml:x}: {len_be} (0x{len_be:x})")
print(data[start_qml:start_qml+len_be].decode('utf-8', errors='replace'))

