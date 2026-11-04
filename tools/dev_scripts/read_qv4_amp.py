with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import struct

# The string "/Pages/ModuleEditors/Amp.qml" is at 0x2d0f818 (UTF-16BE)
pos = data.find(b'/\x00P\x00a\x00g\x00e\x00s\x00/\x00M\x00o\x00d\x00u\x00l\x00e\x00E\x00d\x00i\x00t\x00o\x00r\x00s\x00/\x00A\x00m\x00p\x00.\x00q\x00m\x00l')
print("Position:", hex(pos))

# In QV4 registration, let's find the struct pointing to pos (vaddr = pos + 0x8000)
pos_vaddr = pos + 0x8000
for i in range(0x2c00000, 0x2e00000, 4):
    v = struct.unpack('<I', data[i:i+4])[0]
    if v == pos_vaddr:
        print(f"Found pointer to Amp.qml at {hex(i)}")
        # Print the QV4 unit struct
        for j in range(i-16, i+32, 4):
            val = struct.unpack('<I', data[j:j+4])[0]
            print(f"  {hex(j)}: {hex(val)}")

