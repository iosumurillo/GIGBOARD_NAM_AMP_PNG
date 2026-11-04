import zlib

with open('scratch/decompressed_qml/qml_025_1852310.qml', 'rb') as f:
    orig = f.read()

old_part = (
    b'\t\tImage {\r\n'
    b'\t\t\tid: stompBody\r\n'
    b'\t\t\tx: -15\r\n'
    b'\t\t\tsource: "../../img/FXModule_Active_3_PedalBody.png"\r\n'
    b'\t\t\tvisible: false\r\n'
    b'\t\t}\r\n\r\n'
    b'\t\t Colorize {\r\n'
    b'\t\t\tanchors.fill: stompBody\r\n'
    b'\t\t\tsource: stompBody\r\n'
    b'\t\t\thue: hslColor[0] \r\n'
    b'\t\t\tsaturation: hslColor[1]\r\n'
    b'\t\t\tlightness: hslColor[2] \r\n'
    b'\t\t\topacity: theColor.a \r\n'
    b'\t\t\tcached: true\r\n'
    b'\t\t}'
)

new_part = (
    b'\t\tImage {\r\n'
    b'\t\t\tid: stompBody\r\n'
    b'\t\t\tanchors.centerIn: parent\r\n'
    b'\t\t\twidth: 140\r\n'
    b'\t\t\theight: 220\r\n'
    b'\t\t\tfillMode: Image.PreserveAspectFit\r\n'
    b'\t\t\tsource: "../../Pages/ModuleEditors/img/" + signalChainModule.moduleTypeName.replace(" 2", "") + ".png"\r\n'
    b'\t\t\tvisible: true\r\n'
    b'\t\t}'
)

mod_base = orig.replace(old_part, new_part)
old_text = b'visible: !ampOrCab() && !signalChainModule.isIR'
new_text = b'visible: stompBody.status !== Image.Ready && !ampOrCab() && !signalChainModule.isIR'
mod_base = mod_base.replace(old_text, new_text)

comment_to_remove = b'// signalChainModule.effectType == 1 ? 24 : 31 // MR was 34, but unless we have something to show "Stereo Doubler" correctly in the given rect, 31 is better than an odd word-wrap'
mod_base = mod_base.replace(comment_to_remove, b'')

found = False
for n in (86, 87, 88):
    base_rnd = [(i * 53 + 7) % 94 + 33 for i in range(n)]
    for char in range(33, 126):
        if char in (ord('*'), ord('/')):
            continue
        test_rnd = bytearray(base_rnd)
        test_rnd[-1] = char
        test_bytes = bytes([b for b in test_rnd if b not in (ord('*'), ord('/'))])
        test = mod_base + b'/*' + test_bytes + b'*/'
        test += b' ' * (15288 - len(test))
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
    print('Trying varying other positions...')
    for n in (87, 88):
        base_rnd = [(i * 53 + 7) % 94 + 33 for i in range(n)]
        for pos in range(len(base_rnd)):
            for char in range(33, 126):
                if char in (ord('*'), ord('/')):
                    continue
                test_rnd = bytearray(base_rnd)
                test_rnd[pos] = char
                test_bytes = bytes([b for b in test_rnd if b not in (ord('*'), ord('/'))])
                test = mod_base + b'/*' + test_bytes + b'*/'
                test += b' ' * (15288 - len(test))
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
