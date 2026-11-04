import os, subprocess

# In release/ or scratch/, do we have rootfs.bin?
print('release/rootfs.bin exists:', os.path.exists('release/rootfs.bin'))
if os.path.exists('release/rootfs.bin'):
    print('Size:', os.path.getsize('release/rootfs.bin'))

# In WSL, can we mount it or inspect files?
# Or 7z l release/rootfs.bin
out = subprocess.check_output([r'release/7z.exe', 'l', r'release/rootfs.bin'])
lines = out.decode(errors='replace').splitlines()
print(f'Total files in rootfs.bin: {len(lines)}')
# Search for png, Anxiety, qml, etc.
for l in lines:
    if any(k in l.lower() for k in ['anxiety', 'pedal', 'image', 'stomp', 'lead 800', '.rcc']):
        print(l)

