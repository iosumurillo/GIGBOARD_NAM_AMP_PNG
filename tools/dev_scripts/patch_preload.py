with open('c:/Antigravity/HEADRUSH/patch/nam_preload.cpp', 'r', encoding='utf-8') as f:
    c = f.read()

target = 'install_one_hook(lib, "nam_process_gonk", "NAM_HOOK_SLOT_GONK_V2_ADDR");'
replacement = 'install_one_hook(lib, "nam_process_gonk", "NAM_HOOK_SLOT_GONK_V2_ADDR");\n  install_one_hook(lib, "nam_process_amp", "NAM_HOOK_SLOT_AMP_ADDR");'

assert target in c, "target not found!"
c = c.replace(target, replacement)

with open('c:/Antigravity/HEADRUSH/patch/nam_preload.cpp', 'w', encoding='utf-8') as f:
    f.write(c)

print("nam_preload.cpp patched successfully!")

