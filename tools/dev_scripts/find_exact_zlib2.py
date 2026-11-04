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

# Search for exact 2735 bytes compressed and 15288 uncompressed
for n in range(25, 60):
    for trial in range(500):
        rnd = bytes([b for b in os.urandom(n) if b not in b'*/\r\n\x00'])
        comment = b'/*' + rnd + b'*/'
        test_qml = mod_base + comment
        diff = 15288 - len(test_qml)
        if diff >= 0:
            test_qml += b' ' * diff
            for lvl in (8, 9):
                c = zlib.compress(test_qml, lvl)
                if len(c) == 2735:
                    print(f'EXACT MATCH FOUND! n={n}, lvl={lvl}, len(test_qml)={len(test_qml)}, len(comp)={len(c)}')
                    with open('scratch/ActiveStomp_perfect_patch.bin', 'wb') as out:
                        out.write(c)
                    with open('scratch/ActiveStomp_patched.qml', 'wb') as out:
                        out.write(test_qml)
                    exit(0)

print("Not found in range")

