with open('c:/Antigravity/HEADRUSH/core/model_targets.h', 'r', encoding='utf-8') as f:
    c = f.read()

target = '''  uint32_t v2_engine_vtable_vaddr;
  uint32_t v2_orig_process_fn;

  int qml_rename_count;'''

replacement = '''  uint32_t v2_engine_vtable_vaddr;
  uint32_t v2_orig_process_fn;

  /* Custom PreAmp hijack (Marshall JCM800 LEAD 800 Bright) */
  uint32_t amp_engine_vtable_vaddr;
  uint32_t amp_orig_process_fn;

  int qml_rename_count;'''

assert target in c, "target not found!"
c = c.replace(target, replacement)

with open('c:/Antigravity/HEADRUSH/core/model_targets.h', 'w', encoding='utf-8') as f:
    f.write(c)

print("model_targets.h updated successfully")

