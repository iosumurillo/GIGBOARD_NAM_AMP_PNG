with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

start = 0x1837d1e
length = 419
orig = data[start:start+length]
print("Orig length:", len(orig))
print(repr(orig[:60]))
print(repr(orig[-60:]))

