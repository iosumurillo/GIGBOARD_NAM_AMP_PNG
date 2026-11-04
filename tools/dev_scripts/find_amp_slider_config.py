with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

# Let's search for arrays of 28 elements (or 37 elements) where element 27 is 82 LEAD 800 Bright
# Or look at where amp_type (0..27) is used as an index into a table!
import struct

# In 13a10c: cmp r3, #49
# In 139464: cmp r3, #49
# Let's search for 'cmp r*, #49' or '#31' or '#27' or '#0x1b'
import subprocess

cmd = "/opt/toolchain/bin/arm-buildroot-linux-gnueabihf-objdump -d /mnt/c/Antigravity/HEADRUSH/scratch/Evil_gigboard | grep -E 'cmp.*#(27|49|0x1b|0x31)' | head -n 30"
res = subprocess.run(["wsl", "-d", "Ubuntu", "bash", "-c", cmd], capture_output=True, text=True)
print(res.stdout)

