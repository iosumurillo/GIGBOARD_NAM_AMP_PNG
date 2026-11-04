with open('core/model_targets.c', 'rb') as f:
    c = f.read()

old_block = b'''    .amp_engine_vtable_vaddr = 0x15ec3d8,
    .amp_orig_process_fn = 0x12b318,
    .qml_rename_count = 5,
    .qml_renames =
      {
        {0x1560ed8, "82 LEAD 800 Bright", "82 LEAD 800 (NAM) "},
        {0x15613ac, "GainB", "Model"},
        {0x15613a4, "GainA", "Input"},
        {0x1561374, "Bright", "Tight "},
        {0x15613cc, "Master", "Output"},
      },'''

new_block = b'''    .amp_engine_vtable_vaddr = 0x15ec3d8,
    .amp_orig_process_fn = 0x13a0a0,
    .amp_process_slot = 7,
    .qml_rename_count = 1,
    .qml_renames =
      {
        {0x1560ed8, "82 LEAD 800 Bright", "82 LEAD 800 (NAM) "},
      },'''

if b'\r\n' in c:
    old_block = old_block.replace(b'\n', b'\r\n')
    new_block = new_block.replace(b'\n', b'\r\n')

assert old_block in c, "old_block not found in model_targets.c"
c = c.replace(old_block, new_block, 1)
with open('core/model_targets.c', 'wb') as f:
    f.write(c)
print("Updated core/model_targets.c successfully")

