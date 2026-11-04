import re

with open('scratch/Update.img', 'rb') as f:
    data = f.read()

print('Searching for .qmlc in Update.img...')
matches = re.findall(b'[a-zA-Z0-9_/.-]+\\.qmlc', data)
print('Found .qmlc files:', set(matches[:20]))

print('Searching for .qml files in Update.img...')
qml_matches = re.findall(b'/usr/[a-zA-Z0-9_/.-]+\\.qml', data)
print('Found /usr/*.qml files:', set(qml_matches[:20]))
