# 1. Update model_targets.h
with open('c:/Antigravity/HEADRUSH/core/model_targets.h', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('#define NAM_MAX_QML_RENAMES 4', '#define NAM_MAX_QML_RENAMES 8')
with open('c:/Antigravity/HEADRUSH/core/model_targets.h', 'w', encoding='utf-8') as f:
    f.write(c)
print("model_targets.h updated NAM_MAX_QML_RENAMES")

# 2. Update model_targets.c for gigboard
with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    c = f.read()

target_gig = '''  {
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

rep_gig = '''  {
    .name = "gigboard",
    .match_compatible = "inmusic,hg02",
    .engine_vtable_vaddr = 0x17f2234,
    .orig_process_fn = 0x302840,
    .v2_engine_vtable_vaddr = 0x17f22b0,
    .v2_orig_process_fn = 0x302840,
    .amp_engine_vtable_vaddr = 0x17f20bc,
    .amp_orig_process_fn = 0x2f4fe8,
    .qml_rename_count = 1,
    .qml_renames =
      {
        {
          0x1837d1e,
          "import \\"../Buttons\\"\\r\\n\\r\\nimport QtQuick 2.2\\r\\nimport QtQuick.Controls 1.2\\r\\nimport StateMap 1.0\\r\\n\\r\\nLAStateMapButton {\\r\\n\\twidth: 78; height: 44;\\r\\n\\tframeWidth: 78\\r\\n\\tframeHeight: 44;\\r\\n\\t\\r\\n\\ttoggle: false\\r\\n\\r\\n\\tproperty int index\\r\\n\\tprop: Evil.getProperty(\\"/Engine/RedirCtrl/ModuleSelected%1\\".arg(index+1)); \\r\\n\\ttypeProp: Evil.getProperty(\\"/Engine/Patch/Chain/ModuleType%1\\".arg(index+1)); \\r\\n\\r\\n\\tsource: \\"../img/ModuleButton.png\\";\\r\\n}\\r\\n\\r\\n",
          "import QtQuick 2.2\\nimport StateMap 1.0\\nLAStateMapButton{width:78;height:44;frameWidth:78;frameHeight:44;toggle:false\\nproperty int index\\nprop:Evil.getP(\\"/Engine/RedirCtrl/ModuleSelected\\"+(index+1))\\ntypeProp:Evil.getP(\\"/Engine/Patch/Chain/ModuleType\\"+(index+1))\\nsource:\\"../img/ModuleButton.png\\"\\nImage{anchors.fill:parent;fillMode:1;source:\\"../img/82 LEAD 800 Bright.png\\";visible:typeProp.translator.text===\\"Amp\\"}\\n}\\n\\n\\n\\n\\n\\n\\n"
        },
      },
  },'''

assert target_gig in c, "target_gig not found!"
c = c.replace(target_gig, rep_gig)
with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'w', encoding='utf-8') as f:
    f.write(c)
print("model_targets.c updated with gigboard QML replacement")

# 3. Update patch_pipeline.c
with open('c:/Antigravity/HEADRUSH/core/patch_pipeline.c', 'r', encoding='utf-8') as f:
    c = f.read()

target_pipe = '''    report(progress, progress_user_data, "OK  ELF hijack patched (Anxiety OD V2): trampoline @ 0x%x, hook_slot @ 0x%x",
           elf_result_v2.trampoline_vaddr, elf_result_v2.hook_slot_addr);
  }

  if (target->qml_rename_count > 0)'''

rep_pipe = '''    report(progress, progress_user_data, "OK  ELF hijack patched (Anxiety OD V2): trampoline @ 0x%x, hook_slot @ 0x%x",
           elf_result_v2.trampoline_vaddr, elf_result_v2.hook_slot_addr);
  }

  ElfPatchResult elf_result_amp;
  bool has_amp_hijack = false;
  if (target->amp_engine_vtable_vaddr != 0)
  {
    if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->amp_engine_vtable_vaddr,
                                   target->amp_orig_process_fn, &elf_result_amp, err, err_size))
      goto cleanup;
    has_amp_hijack = true;
    report(progress, progress_user_data, "OK  ELF hijack patched (PreAmp 82 LEAD 800): trampoline @ 0x%x, hook_slot @ 0x%x",
           elf_result_amp.trampoline_vaddr, elf_result_amp.hook_slot_addr);
  }

  if (target->qml_rename_count > 0)'''

assert target_pipe in c, "target_pipe not found!"
c = c.replace(target_pipe, rep_pipe)

target_script = '''  char hook_slot_hex[32];
  snprintf(hook_slot_hex, sizeof(hook_slot_hex), "0x%x", elf_result.hook_slot_addr);
  char hook_slot_v2_hex[32];
  if (has_v2_hijack)
    snprintf(hook_slot_v2_hex, sizeof(hook_slot_v2_hex), "0x%x", elf_result_v2.hook_slot_addr);
  if (!nam_build_launcher_script(script_data, hook_slot_hex, has_v2_hijack ? hook_slot_v2_hex : NULL, &new_script,
                                  err, err_size))
    goto cleanup;'''

rep_script = '''  char hook_slot_hex[32];
  snprintf(hook_slot_hex, sizeof(hook_slot_hex), "0x%x", elf_result.hook_slot_addr);
  char hook_slot_v2_hex[32];
  if (has_v2_hijack)
    snprintf(hook_slot_v2_hex, sizeof(hook_slot_v2_hex), "0x%x", elf_result_v2.hook_slot_addr);
  char hook_slot_amp_hex[32];
  if (has_amp_hijack)
    snprintf(hook_slot_amp_hex, sizeof(hook_slot_amp_hex), "0x%x", elf_result_amp.hook_slot_addr);
  if (!nam_build_launcher_script(script_data, hook_slot_hex, has_v2_hijack ? hook_slot_v2_hex : NULL,
                                 has_amp_hijack ? hook_slot_amp_hex : NULL, &new_script,
                                 err, err_size))
    goto cleanup;'''

assert target_script in c, "target_script not found!"
c = c.replace(target_script, rep_script)

with open('c:/Antigravity/HEADRUSH/core/patch_pipeline.c', 'w', encoding='utf-8') as f:
    f.write(c)
print("patch_pipeline.c updated")

