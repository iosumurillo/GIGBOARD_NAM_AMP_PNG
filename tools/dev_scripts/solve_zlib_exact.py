import zlib

with open('scratch/decompressed_qml/qml_025_1852310.qml', 'rb') as f:
    orig = f.read()

pos1 = orig.find(b'id: stompBody')
pos0 = orig.rfind(b'Image {', 0, pos1)
pos2 = orig.find(b'cached: true', pos1)
pos3 = orig.find(b'}', pos2) + 1

old_body = orig[pos0:pos3]
print("Found old_body len:", len(old_body))

new_body = (
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

mod_base = orig[:pos0] + new_body + orig[pos3:]

old_text = b'visible: !ampOrCab() && !signalChainModule.isIR'
new_text = b'visible: stompBody.status !== Image.Ready && !ampOrCab() && !signalChainModule.isIR'
assert old_text in mod_base, "old_text not found!"
mod_base = mod_base.replace(old_text, new_text)

# Also hide the generic footswitch LED over the realistic pedal
old_led = b'Image {\n\t\t\tx: -15\n\t\t\tsource: signalChainModule.active ? "../../img/FXModule_Active_5_StompSwitchLED.png" : "../../img/FXModule_Bypassed_3_StompSwitchLED.png"\n\t\t}'
new_led = b'Image {\n\t\t\tx: -15\n\t\t\tsource: signalChainModule.active ? "../../img/FXModule_Active_5_StompSwitchLED.png" : "../../img/FXModule_Bypassed_3_StompSwitchLED.png"\n\t\t\tvisible: stompBody.status !== Image.Ready\n\t\t}'
if old_led in mod_base:
    mod_base = mod_base.replace(old_led, new_led)
    print("Generic LED hidden when realistic image is ready!")

# Remove comment to give headroom
comment_to_remove = b'// signalChainModule.effectType == 1 ? 24 : 31 // MR was 34, but unless we have something to show "Stereo Doubler" correctly in the given rect, 31 is better than an odd word-wrap'
mod_base = mod_base.replace(comment_to_remove, b'')

print(f"Base length: {len(mod_base)} (target: 15288)")

found = False
for n in range(50, 120):
    base_rnd = [(i * 53 + 7) % 94 + 33 for i in range(n)]
    for char in range(33, 126):
        if char in (ord('*'), ord('/')):
            continue
        test_rnd = bytearray(base_rnd)
        test_rnd[-1] = char
        test_bytes = bytes([b for b in test_rnd if b not in (ord('*'), ord('/'))])
        test = mod_base + b'/*' + test_bytes + b'*/'
        diff = 15288 - len(test)
        if diff >= 0:
            test += b' ' * diff
            c = zlib.compress(test, 9)
            if len(c) == 2735:
                print(f'MATCH FOUND! n={n}, char={chr(char)}, comp={len(c)}, uncomp={len(test)}')
                with open('scratch/ActiveStomp_perfect_patch.bin', 'wb') as out:
                    out.write(c)
                with open('scratch/ActiveStomp_patched.qml', 'wb') as out:
                    out.write(test)
                found = True
                break
    if found:
        break

if not found:
    print('Searching varied positions...')
    for n in range(70, 110):
        base_rnd = [(i * 53 + 7) % 94 + 33 for i in range(n)]
        for pos in (0, 5, 10, 15, 20):
            for char in range(33, 126):
                if char in (ord('*'), ord('/')):
                    continue
                test_rnd = bytearray(base_rnd)
                test_rnd[pos] = char
                test_bytes = bytes([b for b in test_rnd if b not in (ord('*'), ord('/'))])
                test = mod_base + b'/*' + test_bytes + b'*/'
                diff = 15288 - len(test)
                if diff >= 0:
                    test += b' ' * diff
                    c = zlib.compress(test, 9)
                    if len(c) == 2735:
                        print(f'MATCH FOUND! n={n}, pos={pos}, char={chr(char)}, comp={len(c)}, uncomp={len(test)}')
                        with open('scratch/ActiveStomp_perfect_patch.bin', 'wb') as out:
                            out.write(c)
                        with open('scratch/ActiveStomp_patched.qml', 'wb') as out:
                            out.write(test)
                        found = True
                        break
            if found:
                break
        if found:
            break

