with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re
matches = [m.start() for m in re.finditer(b'BlockDetailsSubPage', data)]
print('Matches for BlockDetailsSubPage:', len(matches))
for m in matches[:10]:
    print(f'At {hex(m)}:', data[m-30:m+70])
