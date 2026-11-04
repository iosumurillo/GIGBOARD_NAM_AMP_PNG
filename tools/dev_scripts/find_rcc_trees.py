with open('scratch/Evil_gigboard', 'rb') as f:
    evil = f.read()

import re

# In Qt RCC, tree nodes have timestamps. Let's find all clusters of timestamps!
# Or let's search for where "Anxiety OD.png" is referenced!
needle = 'Anxiety OD.png'.encode('utf-16-be')
for m in re.finditer(re.escape(needle), evil):
    print(f'Anxiety OD.png at 0x{m.start():x}')

needle_lead = '82 LEAD 800 Bright.png'.encode('utf-16-be')
for m in re.finditer(re.escape(needle_lead), evil):
    print(f'82 LEAD 800 Bright.png at 0x{m.start():x}')

