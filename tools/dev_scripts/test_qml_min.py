qml = '''import QtQuick 2.2
import StateMap 1.0
LAStateMapButton{width:78;height:44;frameWidth:78;frameHeight:44;toggle:false
property int index
prop:Evil.getProperty("/Engine/RedirCtrl/ModuleSelected%1".arg(index+1))
typeProp:Evil.getProperty("/Engine/Patch/Chain/ModuleType%1".arg(index+1))
source:"../img/ModuleButton.png"
Image{anchors.fill:parent;fillMode:Image.PreserveAspectFit;source:"../img/82 LEAD 800 Bright.png";visible:typeProp&&typeProp.translator&&typeProp.translator.text==="Amp"}
}'''

print(f"Length: {len(qml)} bytes (target is 419)")
pad = 419 - len(qml)
print(f"Padding: {pad}")
if pad >= 0:
    qml_padded = qml + (" " * pad)
    print("Exact match 419 bytes!")

