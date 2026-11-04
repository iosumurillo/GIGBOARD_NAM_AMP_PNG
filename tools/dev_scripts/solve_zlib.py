import zlib, os

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

# Remove the long comment at line 561
comment_to_remove = b'// signalChainModule.effectType == 1 ? 24 : 31 // MR was 34, but unless we have something to show "Stereo Doubler" correctly in the given rect, 31 is better than an odd word-wrap'
assert comment_to_remove in mod_base, "comment_to_remove not found!"
mod_base = mod_base.replace(comment_to_remove, b"")

diff_base = 15288 - len(mod_base)
print(f"Base length after trimming: {len(mod_base)} (remaining to target 15288: {diff_base} bytes)")

found = False
for n in range(0, 100):
    for trial in range(1000):
        if n == 0:
            comment = b""
        else:
            rnd = bytes([b for b in os.urandom(n) if b not in b'*/\r\n\x00'])
            comment = b'/*' + rnd + b'*/'
        test_qml = mod_base + comment
        diff = 15288 - len(test_qml)
        if diff >= 0:
            test_qml += b' ' * diff
            for lvl in (6, 7, 8, 9):
                c = zlib.compress(test_qml, lvl)
                if len(c) == 2735 and len(test_qml) == 15288:
                    print(f'EXACT MATCH FOUND! n={n}, trial={trial}, lvl={lvl}, comp={len(c)}, uncomp={len(test_qml)}')
                    with open('scratch/ActiveStomp_perfect_patch.bin', 'wb') as out:
                        out.write(c)
                    with open('scratch/ActiveStomp_patched.qml', 'wb') as out:
                        out.write(test_qml)
                    found = True
                    break
        if found:
            break
    if found:
        break

if not found:
    print('Still searching...')
