with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    c = f.read()

target = '''  {
    .name = "gigboard",
    .match_compatible = "inmusic,hg02",
    .engine_vtable_vaddr = 0x17f2234,
    .orig_process_fn = 0x302840,
    .v2_engine_vtable_vaddr = 0x17f22b0,
    .v2_orig_process_fn = 0x302840,
    .qml_rename_count = 0,
  },'''

replacement = '''  {
    .name = "gigboard",
    .match_compatible = "inmusic,hg02",
    .engine_vtable_vaddr = 0x17f2234,
    .orig_process_fn = 0x302840,
    .v2_engine_vtable_vaddr = 0x17f22b0,
    .v2_orig_process_fn = 0x302840,
    .amp_engine_vtable_vaddr = 0x17f20bc,
    .amp_orig_process_fn = 0x2f4fe8,
    .qml_rename_count = 0,
  },'''

assert target in c, "target not found!"
c = c.replace(target, replacement)

with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'w', encoding='utf-8') as f:
    f.write(c)

print("model_targets.c updated successfully")

