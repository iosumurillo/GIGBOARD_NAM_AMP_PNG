import zlib
import os

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
    b'\t\t\tsource: signalChainModule.type > 0 && signalChainModule.typeProp && signalChainModule.typeProp.translator ? "qrc:/Pages/ModuleEditors/img/" + signalChainModule.typeProp.translator.string.replace(" 2", "") + ".png" : ""\n'
    b'\t\t\tvisible: status === Image.Ready\n'
    b'\t\t}'
)

qml = orig[:pos_start] + new_block + orig[pos_end:]

# Hide text when image is ready
old_text_vis = b'visible: !ampOrCab() && !signalChainModule.isIR'
new_text_vis = b'visible: stompBody.status !== Image.Ready && !ampOrCab() && !signalChainModule.isIR'
qml = qml.replace(old_text_vis, new_text_vis)

# Hide footswitch LED when image is ready
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
qml = qml.replace(old_led, new_led)

comment = b'// signalChainModule.effectType == 1 ? 24 : 31 // MR was 34, but unless we have something to show "Stereo Doubler" correctly in the given rect, 31 is better than an odd word-wrap'
qml = qml.replace(comment, b'')

# Also remove a few comments for headroom
for c in [b'// enabled: signalChainModule.enabled', b'//avoid aliasing of 4x12 cabs', b'// bypass switch']:
    qml = qml.replace(c, b'')

lengths = set()
for _ in range(1000):
    for noise_len in [40, 60, 80, 100]:
        noise = os.urandom(noise_len).replace(b'*', b'A').replace(b'/', b'B')
        cand = qml + b'/*' + noise + b'*/'
        cand += b' ' * (15288 - len(cand))
        for lvl in [6, 7, 8, 9]:
            cl = len(zlib.compress(cand, lvl))
            lengths.add(cl)
            if cl == 2735:
                print(f"FOUND 2735! lvl={lvl}, noise_len={noise_len}")
                with open("scratch/ActiveStomp_patched.qml", "wb") as f:
                    f.write(cand)
                with open("scratch/ActiveStomp_perfect_patch.bin", "wb") as f:
                    f.write(zlib.compress(cand, lvl))
                sys.exit(0)

print('Min:', min(lengths), 'Max:', max(lengths), 'Target 2735 in range:', min(lengths) <= 2735 <= max(lengths))

