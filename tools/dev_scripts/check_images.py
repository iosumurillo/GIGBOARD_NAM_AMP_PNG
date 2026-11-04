import glob
import re
import os

png_found = {}
for path in sorted(glob.glob('scratch/decompressed_qml/*.qml')):
    fname = os.path.basename(path)
    with open(path, 'r', encoding='utf-8', errors='replace') as fp:
        content = fp.read()
    # find image sources
    sources = re.findall(r'source:\s*["\']([^"\']+\.png)["\']', content)
    if sources:
        png_found[fname] = sorted(set(sources))

print(f"QML files with PNG sources: {len(png_found)}")
for k, v in png_found.items():
    print(f"{k}:")
    for s in v:
        print(f"   {s}")
