with open("scratch/Evil_gigboard", "rb") as f:
    data = f.read()

# Let's search for "AnxietyOD.qml" and "AnxietyODV2.qml" contents:
# In RCC, QML files are stored compressed or uncompressed.
# Let's search for snippets like "ModuleEditor" or "stomp" or "Image"
import re
for m in re.finditer(b"AnxietyOD[^\x00]*", data):
    print(f"{hex(m.start())}: {m.group()[:60]}")

