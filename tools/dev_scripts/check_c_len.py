with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# find the string in qml_renames
m = re.search(r'0x1837d1e,\s*"(.*?)",\s*"(.*?)"\s*\},', text, re.DOTALL)
if m:
    s_exp_raw = m.group(1)
    s_new_raw = m.group(2)
    # decode C escape sequences
    s_exp = s_exp_raw.encode('utf-8').decode('unicode_escape')
    s_new = s_new_raw.encode('utf-8').decode('unicode_escape')
    print("Length of C expected:", len(s_exp))
    print("Length of C new:", len(s_new))
    diff = len(s_exp) - len(s_new)
    print("Difference:", diff)

