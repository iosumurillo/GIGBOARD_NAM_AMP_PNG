with open('scratch/ActiveStomp_patched.qml', 'r', encoding='latin1') as f:
    text = f.read()

import re
pos = text.find('id: activeAmp')
print(text[pos:pos+1500])

