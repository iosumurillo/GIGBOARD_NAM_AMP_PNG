with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

# The exact file slice is 419 bytes from 0x1837d1e to 0x1837ec1
actual_bytes = data[0x1837d1e:0x1837ec1]
print("actual_bytes len:", len(actual_bytes))

# Format as C escape
c_expected = ""
for b in actual_bytes:
    if b == ord('\\'):
        c_expected += '\\\\'
    elif b == ord('"'):
        c_expected += '\\"'
    elif b == ord('\r'):
        c_expected += '\\r'
    elif b == ord('\n'):
        c_expected += '\\n'
    elif b == ord('\t'):
        c_expected += '\\t'
    elif 32 <= b <= 126:
        c_expected += chr(b)
    else:
        c_expected += f"\\x{b:02x}"

new_qml = 'import QtQuick 2.2\nimport StateMap 1.0\nLAStateMapButton{width:78;height:44;frameWidth:78;frameHeight:44;toggle:false\nproperty int index\nprop:Evil.getP("/Engine/RedirCtrl/ModuleSelected"+(index+1))\ntypeProp:Evil.getP("/Engine/Patch/Chain/ModuleType"+(index+1))\nsource:"../img/ModuleButton.png"\nImage{anchors.fill:parent;fillMode:1;source:"../img/82 LEAD 800 Bright.png";visible:typeProp.translator.text==="Amp"}\n}'

pad = len(actual_bytes) - len(new_qml)
print("Pad needed:", pad)
assert pad >= 0
new_qml_padded = new_qml + ("\n" * pad)
assert len(new_qml_padded) == len(actual_bytes)

c_new = ""
for b in new_qml_padded.encode('latin1'):
    if b == ord('\\'):
        c_new += '\\\\'
    elif b == ord('"'):
        c_new += '\\"'
    elif b == ord('\r'):
        c_new += '\\r'
    elif b == ord('\n'):
        c_new += '\\n'
    elif b == ord('\t'):
        c_new += '\\t'
    elif 32 <= b <= 126:
        c_new += chr(b)
    else:
        c_new += f"\\x{b:02x}"

with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    c = f.read()

import re
old_block = re.search(r'0x1837d1e,\s*".*?",\s*".*?"\s*\}', c, re.DOTALL).group(0)

replacement_block = f'0x1837d1e,\n          "{c_expected}",\n          "{c_new}"\n        }}'

c = c.replace(old_block, replacement_block)

with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'w', encoding='utf-8') as f:
    f.write(c)

print("model_targets.c updated with byte-perfect expected and new strings!")

