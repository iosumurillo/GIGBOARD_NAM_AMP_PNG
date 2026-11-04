with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

import re
matches = [m.start() for m in re.finditer(b'Pages/ModuleEditors/', data)]
print('Matches count:', len(matches))
seen = set()
for m in matches:
    end = data.find(b'\x00', m)
    s = data[m:end].decode('latin1', errors='ignore')
    if s not in seen:
        seen.add(s)
        if any(k in s.upper() for k in ['AMP', 'LEAD', 'CAB', '82', 'MARSHALL']):
            print(' ', s)

