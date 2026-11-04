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

pad_len = target_uncomp - len(qml)
print(f"Base QML len: {len(qml)}, pad_len: {pad_len}")

found = False
for lvl in [5, 6, 7, 8, 9]:
    for noise_len in range(50, pad_len - 4):
        # Generate pseudo-random noise
        noise = bytearray((i * 47 + 13) % 94 + 33 for i in range(noise_len))
        for idx in range(len(noise)):
            if noise[idx] in (ord('*'), ord('/')):
                noise[idx] = ord('X')
        
        # Vary the last character
        for char in range(33, 126):
            if char in (ord('*'), ord('/')):
                continue
            noise[-1] = char
            candidate = qml + b'/*' + bytes(noise) + b'*/'
            spaces = target_uncomp - len(candidate)
            if spaces >= 0:
                candidate += b' ' * spaces
                comp = zlib.compress(candidate, lvl)
                if len(comp) == target_comp:
                    print(f"SUCCESS! lvl={lvl}, noise_len={noise_len}, char={chr(char)}, comp_len={len(comp)}, uncomp_len={len(candidate)}")
                    with open("scratch/ActiveStomp_patched.qml", "wb") as f:
                        f.write(candidate)
                    with open("scratch/ActiveStomp_perfect_patch.bin", "wb") as f:
                        f.write(comp)
                    found = True
                    break
        if found:
            break
    if found:
        break

if not found:
    print("Searching with seed variation...")
    for lvl in [5, 6, 7, 8, 9]:
        for seed in range(1, 100):
            for noise_len in range(30, pad_len - 4):
                noise = bytearray((i * seed + 19) % 94 + 33 for i in range(noise_len))
                for idx in range(len(noise)):
                    if noise[idx] in (ord('*'), ord('/')):
                        noise[idx] = ord('A')
                candidate = qml + b'/*' + bytes(noise) + b'*/'
                spaces = target_uncomp - len(candidate)
                if spaces >= 0:
                    candidate += b' ' * spaces
                    comp = zlib.compress(candidate, lvl)
                    if len(comp) == target_comp:
                        print(f"SUCCESS! lvl={lvl}, seed={seed}, noise_len={noise_len}, comp_len={len(comp)}")
                        with open("scratch/ActiveStomp_patched.qml", "wb") as f:
                            f.write(candidate)
                        with open("scratch/ActiveStomp_perfect_patch.bin", "wb") as f:
                            f.write(comp)
                        found = True
                        break
            if found:
                break
        if found:
            break

assert found, "Match not found!"
