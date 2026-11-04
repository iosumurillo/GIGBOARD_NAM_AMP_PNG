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
if old_part not in orig:
    old_part = old_part.replace(b'\r\n', b'\n')

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
if b'\r\n' not in orig:
    new_part = new_part.replace(b'\r\n', b'\n')

mod_base = orig.replace(old_part, new_part)
old_text = b'visible: !ampOrCab() && !signalChainModule.isIR'
new_text = b'visible: stompBody.status !== Image.Ready && !ampOrCab() && !signalChainModule.isIR'
mod_base = mod_base.replace(old_text, new_text)

# We want compressed length == 2735 and uncompressed length == 15288
found = False
import random
random.seed(42)

for lvl in range(1, 10):
    for pad in range(0, 300):
        # vary padding with different entropy
        pad_str = b' //' + bytes([(i * 37 + 13) % 26 + ord('a') for i in range(pad)])
        test_qml = mod_base + pad_str
        diff = 15288 - len(test_qml)
        if diff >= 0:
            test_qml += b' ' * diff
        else:
            continue
        c = zlib.compress(test_qml, lvl)
        if len(c) == 2735 and len(test_qml) == 15288:
            print(f'FOUND! lvl={lvl}, pad={pad}, uncomp={len(test_qml)}, comp={len(c)}')
            with open('scratch/ActiveStomp_perfect_patch.bin', 'wb') as out:
                out.write(c)
            with open('scratch/ActiveStomp_patched.qml', 'wb') as out:
                out.write(test_qml)
            found = True
            break
    if found:
        break

if not found:
    print('Testing pseudo-random padding...')
    for attempt in range(50000):
        pad = random.randint(10, 200)
        pad_str = b' //' + bytes([random.randint(32, 126) for _ in range(pad)])
        test_qml = mod_base + pad_str
        diff = 15288 - len(test_qml)
        if diff >= 0:
            test_qml += b' ' * diff
        else:
            continue
        lvl = random.randint(6, 9)
        c = zlib.compress(test_qml, lvl)
        if len(c) == 2735 and len(test_qml) == 15288:
            print(f'FOUND randomized! attempt={attempt}, lvl={lvl}, pad={pad}')
            with open('scratch/ActiveStomp_perfect_patch.bin', 'wb') as out:
                out.write(c)
            with open('scratch/ActiveStomp_patched.qml', 'wb') as out:
                out.write(test_qml)
            found = True
            break

