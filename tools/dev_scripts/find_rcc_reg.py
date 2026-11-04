import struct

with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

# Let's search for 0x298e8da in the entire binary, or search for name_off
# In Qt RCC, tree nodes are 22 bytes:
# uint32_t name_offset;
# uint16_t flags;
# uint32_t child_count (or 1 if file);
# uint32_t data_offset (or child_offset if dir);
# uint64_t timestamp;

# Notice the timestamp: 8 bytes.
# Let's find all tree nodes in the binary by searching for 8-byte timestamps or checking tree_base
# Where is tree_base registered in Evil?
# In Qt RCC, qRegisterResourceData(int version, const unsigned char *tree, const unsigned char *names, const unsigned char *data)
# Let's search for calls or references to qRegisterResourceData in Evil!

# Let's search for string 'qRegisterResourceData' or '_Z21qRegisterResourceData'
import re
for m in re.finditer(b'qRegisterResourceData', data):
    print('Found string at', hex(m.start()))

