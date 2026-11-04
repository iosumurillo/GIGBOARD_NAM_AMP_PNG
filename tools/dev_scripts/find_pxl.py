import os

search_roots = [
    r'c:\Antigravity',
    r'C:\Users\iosum\Downloads',
    r'C:\Users\iosum\Desktop',
    r'C:\Users\iosum\Pictures',
    r'C:\Users\iosum\Documents',
    r'C:\Users\iosum\OneDrive',
    r'C:\Users\iosum\.gemini',
]

for s in search_roots:
    if os.path.exists(s):
        for root, dirs, files in os.walk(s):
            for f in files:
                if '20261102' in f or 'PXL' in f:
                    print(os.path.join(root, f))

