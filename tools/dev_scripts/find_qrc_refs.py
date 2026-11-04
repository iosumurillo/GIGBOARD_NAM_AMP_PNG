import glob, re
qrc_refs = set()
for f in glob.glob('scratch/decompressed_qml/*.qml'):
    with open(f, 'r', encoding='utf-8', errors='replace') as fp:
        c = fp.read()
    for m in re.findall(r'qrc:/[^"\'\s)]+', c):
        qrc_refs.add(m)

print(f"Total qrc references: {len(qrc_refs)}")
for r in sorted(qrc_refs):
    print(" ", r)

