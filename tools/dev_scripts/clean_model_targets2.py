with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    c = f.read()

bad = '''          "import QtQuick 2.2\\nimport StateMap 1.0\\nLAStateMapButton{width:78;height:44;frameWidth:78;frameHeight:44;toggle:false\\nproperty int index\\nprop:Evil.getP(\\"/Engine/RedirCtrl/ModuleSelected\\"+(index+1))\\ntypeProp:Evil.getP(\\"/Engine/Patch/Chain/ModuleType\\"+(index+1))\\nsource:\\"../img/ModuleButton.png\\"\\nImage{anchors.fill:parent;fillMode:1;source:\\"../img/82 LEAD 800 Bright.png\\";visible:typeProp.translator.text===\\"Amp\\"}\\n}\\n\\n\\n\\n\\n\\n\\n"
        }\\n}\\n\\n\\n\\n\\n\\n\\n"'''

good = '''          "import QtQuick 2.2\\nimport StateMap 1.0\\nLAStateMapButton{width:78;height:44;frameWidth:78;frameHeight:44;toggle:false\\nproperty int index\\nprop:Evil.getP(\\"/Engine/RedirCtrl/ModuleSelected\\"+(index+1))\\ntypeProp:Evil.getP(\\"/Engine/Patch/Chain/ModuleType\\"+(index+1))\\nsource:\\"../img/ModuleButton.png\\"\\nImage{anchors.fill:parent;fillMode:1;source:\\"../img/82 LEAD 800 Bright.png\\";visible:typeProp.translator.text===\\"Amp\\"}\\n}\\n\\n\\n\\n\\n\\n\\n"'''

assert bad in c, "bad not found"
c = c.replace(bad, good)

with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'w', encoding='utf-8') as f:
    f.write(c)

print("model_targets.c fixed line 52 deleted")

