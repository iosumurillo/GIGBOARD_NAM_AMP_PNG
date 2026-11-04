with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

def find_all(pattern):
    idx = 0
    while True:
        pos = data.find(pattern, idx)
        if pos == -1:
            break
        print(f"Found {pattern} at 0x{pos:x} (len {len(pattern)})")
        # print context
        start = max(0, pos - 64)
        end = min(len(data), pos + len(pattern) + 64)
        print("  Context:", repr(data[start:end]))
        idx = pos + len(pattern)

print("Searching ModuleButton.png:")
find_all(b'ModuleButton.png')

print("\nSearching LEAD 800:")
find_all(b'LEAD 800')

print("\nSearching LAStateMapButton:")
find_all(b'LAStateMapButton')

