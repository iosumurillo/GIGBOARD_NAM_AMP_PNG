import zlib

with open('scratch/decompressed_qml/qml_025_1852310.qml', 'rb') as f:
    orig_qml = f.read()

print(f"Original uncompressed size: {len(orig_qml)}")

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

if old_part not in orig_qml:
    # try with \n
    old_part = old_part.replace(b'\r\n', b'\n')

assert old_part in orig_qml, "old_part not found!"

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
if b'\r\n' not in orig_qml:
    new_part = new_part.replace(b'\r\n', b'\n')

mod_qml = orig_qml.replace(old_part, new_part)

old_text = b'visible: !ampOrCab() && !signalChainModule.isIR'
new_text = b'visible: stompBody.status !== Image.Ready && !ampOrCab() && !signalChainModule.isIR'
assert old_text in mod_qml, "old_text not found!"
mod_qml = mod_qml.replace(old_text, new_text)

# Also adjust original size by padding comments if we want exact uncompressed length:
diff_uncompressed = len(orig_qml) - len(mod_qml)
print(f"Uncompressed len diff: {diff_uncompressed}")
if diff_uncompressed > 0:
    mod_qml += b' ' * diff_uncompressed
elif diff_uncompressed < 0:
    print(f"Mod is larger by {-diff_uncompressed} bytes")

print(f"Final uncompressed len: {len(mod_qml)} (orig: {len(orig_qml)})")

comp = zlib.compress(mod_qml, 9)
print(f"Compressed size at level 9: {len(comp)} bytes (original slot: 2735 bytes)")
pad_compressed = 2735 - len(comp)
print(f"Compressed diff (slot - compressed): {pad_compressed}")

