qml = '''import QtQuick 2.2
import StateMap 1.0
LAStateMapButton{width:78;height:44;frameWidth:78;frameHeight:44;toggle:false
property int index
prop:Evil.getP("/Engine/RedirCtrl/ModuleSelected"+(index+1))
typeProp:Evil.getP("/Engine/Patch/Chain/ModuleType"+(index+1))
source:"../img/ModuleButton.png"
Image{anchors.fill:parent;fillMode:1;source:"../img/82 LEAD 800 Bright.png";visible:typeProp.translator.text==="Amp"}
}'''

print(f"Length: {len(qml)} bytes (target is 419)")
pad = 419 - len(qml)
print(f"Padding: {pad}")
if pad >= 0:
    qml_padded = qml + ("\n" * pad)
    print(f"PERFECT! Length is exactly {len(qml_padded)} bytes!")

