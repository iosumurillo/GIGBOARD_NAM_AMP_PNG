with open("scratch/Evil_gigboard", "rb") as f:
    data = f.read()

import re

# Search for the string "Pages/ModuleEditors"
for m in re.finditer(b"Pages/ModuleEditors[^\x00]*", data):
    print(f"Match at {hex(m.start())}: {m.group()}")
