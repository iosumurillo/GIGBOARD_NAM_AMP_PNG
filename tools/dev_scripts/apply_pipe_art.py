with open('core/patch_pipeline.c', 'rb') as f:
    data = f.read()

target = b'           target->name);\r\n  }\r\n\r\n  char hook_slot_hex[32];'
replacement = (
    b'           target->name);\r\n  }\r\n\r\n'
    b'  /* Patch ActiveStomp.qml to replace generic colored blocks with pedal artwork */\r\n'
    b'  {\r\n'
    b'    const uint8_t needle[] = {0x00, 0x00, 0x3b, 0xb8, 0x78, 0x9c};\r\n'
    b'    size_t needle_len = sizeof(needle);\r\n'
    b'    bool patched_artwork = false;\r\n'
    b'    for (size_t i = 0; i + needle_len + ACTIVE_STOMP_PATCH_LEN <= evil_len; ++i)\r\n'
    b'    {\r\n'
    b'      if (memcmp(evil_data + i, needle, needle_len) == 0)\r\n'
    b'      {\r\n'
    b'        memcpy(evil_data + i + 4, ACTIVE_STOMP_PATCH, ACTIVE_STOMP_PATCH_LEN);\r\n'
    b'        report(progress, progress_user_data, "OK  ActiveStomp.qml patched with realistic pedal artwork @ 0x%zx", i + 4);\r\n'
    b'        patched_artwork = true;\r\n'
    b'        break;\r\n'
    b'      }\r\n'
    b'    }\r\n'
    b'    if (!patched_artwork)\r\n'
    b'    {\r\n'
    b'      report(progress, progress_user_data, "    (ActiveStomp.qml artwork needle not found, skipped)");\r\n'
    b'    }\r\n'
    b'  }\r\n\r\n'
    b'  char hook_slot_hex[32];'
)

assert target in data, 'target not found!'
data = data.replace(target, replacement)

with open('core/patch_pipeline.c', 'wb') as f:
    f.write(data)

print('Successfully patched core/patch_pipeline.c!')

