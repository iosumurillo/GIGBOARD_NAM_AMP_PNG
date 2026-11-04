with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

pos = 0x1837d7d
start_import = data.rfind(b'import QtQuick 2.2', 0, pos)
print(f"start_import at 0x{start_import:x}")
chunk = data[start_import-16:start_import+16]
print("Hex before start_import:", " ".join(f"{b:02x}" for b in chunk))

