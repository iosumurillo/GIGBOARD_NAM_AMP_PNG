with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Line 50:", repr(lines[50]))
print("Line 51:", repr(lines[51]))
print("Line 52:", repr(lines[52]))
print("Line 53:", repr(lines[53]))

# Delete line 51 (the corrupted line 52)
del lines[51]

with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Line deleted successfully!")

