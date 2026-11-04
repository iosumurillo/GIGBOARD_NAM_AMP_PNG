with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

def show_around(pos, name):
    print(f"=== {name} at 0x{pos:x} ===")
    start = max(0, pos - 200)
    end = min(len(data), pos + 2500)
    chunk = data[start:end]
    print(chunk.decode('utf-8', errors='replace'))

show_around(0x156bc54, "BlockDetails.qml")
show_around(0x18494a8, "SignalChaninModule.qml")

