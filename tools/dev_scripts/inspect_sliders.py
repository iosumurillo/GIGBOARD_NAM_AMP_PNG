with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

# Let's search around 0x15e2764 for amp configurations
# Look at 0x15e0000 to 0x15e4000
import re

# Let's find references to "82 Lead" or amp indices
# Index 27 is 82 LEAD 800 Bright
# Let's inspect where sld7, sld8, etc. are used in data structures
pos = 0x15e2764
print("Context around 0x15e2764:")
print(data[pos-100:pos+200])

