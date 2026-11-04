with open('c:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    data = f.read()

with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'0x1837d1e,\s*"(.*?)",', text, re.DOTALL)
expected = m.group(1).encode('utf-8').decode('unicode_escape').encode('latin1')

actual = data[0x1837d1e:0x1837d1e+len(expected)]
print("len(expected):", len(expected))
print("len(actual):", len(actual))

for i in range(min(len(expected), len(actual))):
    if expected[i] != actual[i]:
        print(f"Mismatch at index {i} (offset 0x{0x1837d1e+i:x}): expected {expected[i]:#x} ({repr(chr(expected[i]))}), actual {actual[i]:#x} ({repr(chr(actual[i]))})")
        print("Expected context:", repr(expected[max(0, i-10):i+20]))
        print("Actual context:  ", repr(actual[max(0, i-10):i+20]))
        break
else:
    print("Full match!")

