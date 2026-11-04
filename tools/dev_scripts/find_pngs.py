import re

with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

# Find strings ending in .png
png_matches = set(re.findall(b'([a-zA-Z0-9_/ -]+\\.png)', data))
print(f"Found {len(png_matches)} png matches")
for m in sorted(png_matches):
    if b'LEAD' in m or b'Lead' in m or b'800' in m or b'Bright' in m or b'Amp' in m or b'amp' in m or b'Module' in m:
        print(" ", m.decode('utf-8', errors='replace'))

