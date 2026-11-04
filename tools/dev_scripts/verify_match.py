with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

expected = b'import "../Buttons"\r\n\r\nimport QtQuick 2.2\r\nimport QtQuick.Controls 1.2\r\nimport StateMap 1.0\r\n\r\nLAStateMapButton {\r\n\twidth: 78; height: 44;\r\n\tframeWidth: 78\r\n\tframeHeight: 44\r\n\t\r\n\ttoggle: false\r\n\r\n\tproperty int index\r\n\tprop: Evil.getProperty("/Engine/RedirCtrl/ModuleSelected%1".arg(index+1)); \r\n\ttypeProp: Evil.getProperty("/Engine/Patch/Chain/ModuleType%1".arg(index+1)); \r\n\r\n\tsource: "../img/ModuleButton.png";\r\n}\r\n\r\n'

replacement = b'import QtQuick 2.2\nimport StateMap 1.0\nLAStateMapButton{width:78;height:44;frameWidth:78;frameHeight:44;toggle:false\nproperty int index\nprop:Evil.getP("/Engine/RedirCtrl/ModuleSelected"+(index+1))\ntypeProp:Evil.getP("/Engine/Patch/Chain/ModuleType"+(index+1))\nsource:"../img/ModuleButton.png"\nImage{anchors.fill:parent;fillMode:1;source:"../img/82 LEAD 800 Bright.png";visible:typeProp.translator.text==="Amp"}\n}\n\n\n\n\n\n\n'

print("len(expected):", len(expected))
print("len(replacement):", len(replacement))
assert len(expected) == len(replacement)

actual = data[0x1837d1e:0x1837d1e+len(expected)]
print("Matches Evil_gigboard exactly?", actual == expected)

