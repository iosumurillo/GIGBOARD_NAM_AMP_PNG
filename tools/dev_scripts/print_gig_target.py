with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    c = f.read()

import re
# Let's inspect qml_renames for gigboard
start = c.find('.name = "gigboard"')
end = c.find('};\n\nstatic const ModelTarget* find_by_name', start)
print(c[start:end])

