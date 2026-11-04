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

# Remove comments for headroom
comments_to_remove = [
    b'// signalChainModule.effectType == 1 ? 24 : 31 // MR was 34, but unless we have something to show "Stereo Doubler" correctly in the given rect, 31 is better than an odd word-wrap',
    b'// enabled: signalChainModule.enabled',
    b'//avoid aliasing of 4x12 cabs',
    b'// bypass switch',
    b'//first amp',
    b'// doubled amp',
    b'//first cab',
    b'// doubled cab',
    b'//main / upper IR',
    b'// doubled IR'
]
for c in comments_to_remove:
    qml = qml.replace(c, b'')

target_uncomp = len(orig) # 15288
target_comp = 2735

headroom = target_uncomp - len(qml)
print(f"Target uncompressed: {target_uncomp}, current QML: {len(qml)}, headroom: {headroom}")

found = False
for lvl in [9, 8, 7, 6]:
    for n in range(1, min(headroom - 4, 180)):
        base_noise = [(i * 53 + 7) % 94 + 33 for i in range(n)]
        for char in range(33, 126):
            if char in (ord('*'), ord('/')):
                continue
            test_noise = bytearray(base_noise)
            test_noise[-1] = char
            noise_bytes = bytes([b for b in test_noise if b not in (ord('*'), ord('/'))])
            candidate = qml + b'/*' + noise_bytes + b'*/'
            diff = target_uncomp - len(candidate)
            if diff >= 0:
                candidate += b' ' * diff
                comp = zlib.compress(candidate, lvl)
                if len(comp) == target_comp:
                    print(f"EXACT MATCH FOUND at lvl {lvl}! noise_len={n}, char={chr(char)}, comp={len(comp)}, uncomp={len(candidate)}")
                    with open("scratch/ActiveStomp_patched.qml", "wb") as out_f:
                        out_f.write(candidate)
                    with open("scratch/ActiveStomp_perfect_patch.bin", "wb") as out_f:
                        out_f.write(comp)
                    found = True
                    break
        if found:
            break
    if found:
        break

assert found, "Could not find exact 2735-byte match!"
print("Done!")
