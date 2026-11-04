import zlib

with open('scratch/decompressed_qml/qml_025_1852310.qml', 'rb') as f:
    orig = f.read()

pos_body = orig.find(b'id: stompBody')
pos_start = orig.rfind(b'Image {', 0, pos_body)
pos_cached = orig.find(b'cached: true', pos_body)
pos_end = orig.find(b'}', pos_cached) + 1

new_block = (
    b'Image {\n'
    b'\t\t\tid: stompBody\n'
    b'\t\t\tanchors.centerIn: parent\n'
    b'\t\t\twidth: 140\n'
    b'\t\t\theight: 220\n'
    b'\t\t\tfillMode: Image.PreserveAspectFit\n'
    b'\t\t\tsource: "../../Pages/ModuleEditors/img/" + signalChainModule.moduleTypeName.replace(" 2", "") + ".png"\n'
    b'\t\t\tvisible: true\n'
    b'\t\t}'
)

qml = orig[:pos_start] + new_block + orig[pos_end:]
old_text_vis = b'visible: !ampOrCab() && !signalChainModule.isIR'
new_text_vis = b'visible: stompBody.status !== Image.Ready && !ampOrCab() && !signalChainModule.isIR'
qml = qml.replace(old_text_vis, new_text_vis)

old_led = (
    b'Image {\n'
    b'\t\t\tx: -15\n'
    b'\t\t\tsource: signalChainModule.active ? "../../img/FXModule_Active_5_StompSwitchLED.png" : "../../img/FXModule_Bypassed_3_StompSwitchLED.png"\n'
    b'\t\t}'
)
new_led = (
    b'Image {\n'
    b'\t\t\tx: -15\n'
    b'\t\t\tsource: signalChainModule.active ? "../../img/FXModule_Active_5_StompSwitchLED.png" : "../../img/FXModule_Bypassed_3_StompSwitchLED.png"\n'
    b'\t\t\tvisible: stompBody.status !== Image.Ready\n'
    b'\t\t}'
)
if old_led in qml:
    qml = qml.replace(old_led, new_led)

comment = b'// signalChainModule.effectType == 1 ? 24 : 31 // MR was 34, but unless we have something to show "Stereo Doubler" correctly in the given rect, 31 is better than an odd word-wrap'
qml = qml.replace(comment, b'')

test = qml + b' ' * (15288 - len(qml))
for lvl in range(1, 10):
    c = zlib.compress(test, lvl)
    print(f'lvl {lvl}: comp={len(c)}')

