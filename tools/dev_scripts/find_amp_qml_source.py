import re

with open('scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

name_needle = b'\x00A\x00m\x00p\x00.\x00q\x00m\x00l'
name_matches = [hex(m.start()) for m in re.finditer(re.escape(name_needle), data)]
print('UTF-16 name matches:', name_matches)

# Let's inspect bytes around these matches
for m_str in name_matches:
    m = int(m_str, 16)
    print(f'At {m_str}:', data[m-20:m+40])
