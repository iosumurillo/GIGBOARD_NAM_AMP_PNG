with open('c:/Antigravity/HEADRUSH/core/launcher_script.h', 'r', encoding='utf-8') as f:
    c = f.read()

target = '''bool nam_build_launcher_script(const char* stock_script_text, const char* hook_slot_addr_hex,
                                const char* hook_slot_v2_addr_hex, char** out, char* err, size_t err_size);'''

replacement = '''bool nam_build_launcher_script(const char* stock_script_text, const char* hook_slot_addr_hex,
                                const char* hook_slot_v2_addr_hex, const char* hook_slot_amp_addr_hex,
                                char** out, char* err, size_t err_size);'''

assert target in c, "target not found in launcher_script.h"
c = c.replace(target, replacement)

with open('c:/Antigravity/HEADRUSH/core/launcher_script.h', 'w', encoding='utf-8') as f:
    f.write(c)

print("launcher_script.h updated")

with open('c:/Antigravity/HEADRUSH/core/launcher_script.c', 'r', encoding='utf-8') as f:
    c = f.read()

target1 = '''bool nam_build_launcher_script(const char* stock_script_text, const char* hook_slot_addr_hex,
                                const char* hook_slot_v2_addr_hex, char** out, char* err, size_t err_size)'''

replacement1 = '''bool nam_build_launcher_script(const char* stock_script_text, const char* hook_slot_addr_hex,
                                const char* hook_slot_v2_addr_hex, const char* hook_slot_amp_addr_hex,
                                char** out, char* err, size_t err_size)'''

assert target1 in c, "target1 not found in launcher_script.c"
c = c.replace(target1, replacement1)

target2 = '''  if (hook_slot_v2_addr_hex)
  {
    ok = ok && sb_append_str(&final, " NAM_HOOK_SLOT_GONK_V2_ADDR=");
    ok = ok && sb_append_str(&final, hook_slot_v2_addr_hex);
  }
  ok = ok && sb_append_str(&final, " /usr/Evil/Evil");'''

replacement2 = '''  if (hook_slot_v2_addr_hex)
  {
    ok = ok && sb_append_str(&final, " NAM_HOOK_SLOT_GONK_V2_ADDR=");
    ok = ok && sb_append_str(&final, hook_slot_v2_addr_hex);
  }
  if (hook_slot_amp_addr_hex)
  {
    ok = ok && sb_append_str(&final, " NAM_HOOK_SLOT_AMP_ADDR=");
    ok = ok && sb_append_str(&final, hook_slot_amp_addr_hex);
  }
  ok = ok && sb_append_str(&final, " /usr/Evil/Evil");'''

assert target2 in c, "target2 not found in launcher_script.c"
c = c.replace(target2, replacement2)

with open('c:/Antigravity/HEADRUSH/core/launcher_script.c', 'w', encoding='utf-8') as f:
    f.write(c)

print("launcher_script.c updated")

