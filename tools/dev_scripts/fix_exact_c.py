s_exp = "import \"../Buttons\"\r\n\r\nimport QtQuick 2.2\r\nimport QtQuick.Controls 1.2\r\nimport StateMap 1.0\r\n\r\nLAStateMapButton {\r\n\twidth: 78; height: 44;\r\n\tframeWidth: 78\r\n\tframeHeight: 44;\r\n\t\r\n\ttoggle: false\r\n\r\n\tproperty int index\r\n\tprop: Evil.getProperty(\"/Engine/RedirCtrl/ModuleSelected%1\".arg(index+1)); \r\n\ttypeProp: Evil.getProperty(\"/Engine/Patch/Chain/ModuleType%1\".arg(index+1)); \r\n\r\n\tsource: \"../img/ModuleButton.png\";\r\n}\r\n\r\n"

s_new = "import QtQuick 2.2\nimport StateMap 1.0\nLAStateMapButton{width:78;height:44;frameWidth:78;frameHeight:44;toggle:false\nproperty int index\nprop:Evil.getP(\"/Engine/RedirCtrl/ModuleSelected\"+(index+1))\ntypeProp:Evil.getP(\"/Engine/Patch/Chain/ModuleType\"+(index+1))\nsource:\"../img/ModuleButton.png\"\nImage{anchors.fill:parent;fillMode:1;source:\"../img/82 LEAD 800 Bright.png\";visible:typeProp.translator.text===\"Amp\"}\n}"

print("len(s_exp):", len(s_exp))
print("len(s_new):", len(s_new))
diff = len(s_exp) - len(s_new)
print("Difference needed:", diff)
s_new_padded = s_new + ("\n" * diff)
print("len(s_new_padded):", len(s_new_padded))
assert len(s_new_padded) == len(s_exp)

# Write out the exact replacement
with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    c = f.read()

# build C escaped string for s_new_padded
escaped_new = s_new_padded.replace('\n', '\\n').replace('"', '\\"')

import re
old_block = re.search(r'0x1837d1e,\s*".*?",\s*".*?"\s*\}', c, re.DOTALL).group(0)

# replace the new part
old_parts = old_block.split('",')
new_block = old_parts[0] + '",\n          "' + escaped_new + '"\n        }'

c = c.replace(old_block, new_block)

with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'w', encoding='utf-8') as f:
    f.write(c)

print("Exact match written to model_targets.c")

