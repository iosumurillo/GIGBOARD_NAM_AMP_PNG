with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re
# Let's search for "Amp {" or look for where Amp.qml body starts
matches = [m.start() for m in re.finditer(b'Amp {', data)]
for m in matches:
    print(f'At {hex(m)}:')
    print(data[m:m+500].decode('latin1', errors='ignore'))
    print('='*50)

