with open("scratch/Evil_gigboard", "rb") as f:
    data = f.read()

import struct

name_entry_v1 = 0x298da92
name_entry_v2 = 0x298d8e2

# In Qt, what if name_offset is 2 bytes or 4 bytes?
# In Qt 5 RCC, the tree format:
# struct QtResourceNode {
#     uint32_t name_offset;
#     uint16_t flags;
#     union {
#         struct {
#             uint32_t child_count;
#             uint32_t child_offset;
#         } directory;
#         struct {
#             uint32_t country;
#             uint32_t language;
#             uint32_t data_offset;
#         } file; // or 14/16/24 bytes depending on version
#     };
# };

# But what if there are multiple RCC bundles registered in Evil_gigboard?
# Let's search for the byte sequences:
# 'Anxiety OD.png'
# Let's find every occurrence of off_v1 or relative offsets:
# Let's search for data payload offsets:
# Earlier we found:
# At 0x2180c1a: length=63031 (img_234)
# At 0x2190255: length=75435 (img_235)
# What is data_offset in RCC?
# data_offset is relative to qt_resource_data base!
# What is qt_resource_data base?
# img_001 is at 0x15a13b8 (header at 0x15a13b4).
# If data_base is 0x15a13b4:
data_base = 0x15a13b4
off_data_234 = (0x2180c1a - 4) - data_base
off_data_235 = (0x2190255 - 4) - data_base
print(f"Candidate data offsets: 234={hex(off_data_234)}, 235={hex(off_data_235)}")

for off_val, name in [(off_data_234, "234"), (off_data_235, "235")]:
    b = off_val.to_bytes(4, "big")
    p = 0
    while True:
        p = data.find(b, p)
        if p == -1: break
        print(f"Data offset for {name} found at {hex(p)}: {data[p-12:p+12].hex()}")
        p += 4
