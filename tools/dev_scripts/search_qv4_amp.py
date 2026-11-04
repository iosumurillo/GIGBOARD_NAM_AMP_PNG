import glob

for f in sorted(glob.glob('scratch/decompressed_qml/qml_*.qml')):
    with open(f, 'rb') as fp:
        c = fp.read()
    # Check if this decompressed QML or QV4 file mentions Amp.qml
    if b'Amp.qml' in c or b'ModuleEditors/Amp' in c:
        print(f, "has ModuleEditors/Amp!")
    if b'GainA' in c:
        print(f, "has GainA!")
    if b'GainB' in c:
        print(f, "has GainB!")

