with open('/mnt/c/Antigravity/HEADRUSH/core/patch_pipeline.c', 'rb') as f:
    content = f.read()

target = b'''    if (!patched_artwork)
    {
      report(progress, progress_user_data, "    (ActiveStomp.qml artwork needle not found, skipped)");
    }
  }'''

replacement = b'''    if (!patched_artwork)
    {
      report(progress, progress_user_data, "    (ActiveStomp.qml artwork needle not found, skipped)");
    }

    /* Bypass Qt Quick Compiler (QV4) cache for ActiveStomp.qml so Qt loads patched RCC */
    static const uint8_t qv4_path_needle[] = {
      '/', 0, 'G', 0, 'r', 0, 'o', 0, 'u', 0, 'p', 0, 's', 0, '/', 0,
      'S', 0, 'i', 0, 'g', 0, 'n', 0, 'a', 0, 'l', 0, 'C', 0, 'h', 0, 'a', 0, 'i', 0, 'n', 0,
      'M', 0, 'o', 0, 'd', 0, 'u', 0, 'l', 0, 'e', 0, 'S', 0, 't', 0, 'o', 0, 'm', 0, 'p', 0, 's', 0, '/', 0,
      'A', 0, 'c', 0, 't', 0, 'i', 0, 'v', 0, 'e', 0, 'S', 0, 't', 0, 'o', 0, 'm', 0, 'p', 0,
      '.', 0, 'q', 0, 'm', 0, 'l', 0
    };
    bool bypassed_qv4_path = false;
    for (size_t i = 0; i + sizeof(qv4_path_needle) <= evil_len; ++i)
    {
      if (memcmp(evil_data + i, qv4_path_needle, sizeof(qv4_path_needle)) == 0)
      {
        /* Invalidate registration path: /Groups/.../ActiveStomp -> /Groups/.../XctiveStomp */
        /* 'A' is at byte offset 64 */
        evil_data[i + 64] = 'X';
        report(progress, progress_user_data, "OK  Bypassed QV4 compiled unit registration @ 0x%zx", i);
        bypassed_qv4_path = true;
        break;
      }
    }
    if (!bypassed_qv4_path)
    {
      report(progress, progress_user_data, "    (QV4 ActiveStomp registration needle not found, skipped)");
    }

    /* Also invalidate unit header magic if found so verifyHeader fails */
    static const uint8_t qv4_header_needle[] = {
      'q', 'v', '4', 'c', 'd', 'a', 't', 'a',
      0x29, 0x00, 0x00, 0x00, 0x02, 0x0f, 0x05, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
      0x84, 0xd8, 0x00, 0x00
    };
    bool invalidated_qv4_unit = false;
    for (size_t i = 0; i + sizeof(qv4_header_needle) <= evil_len; ++i)
    {
      if (memcmp(evil_data + i, qv4_header_needle, sizeof(qv4_header_needle)) == 0)
      {
        evil_data[i + 3] = 'x'; /* qv4xdata */
        report(progress, progress_user_data, "OK  Invalidated QV4 ActiveStomp compiled bytecode @ 0x%zx", i);
        invalidated_qv4_unit = true;
        break;
      }
    }
    if (!invalidated_qv4_unit)
    {
      report(progress, progress_user_data, "    (QV4 ActiveStomp bytecode header needle not found, skipped)");
    }
  }'''

if b'\r\n' in content:
    target = target.replace(b'\n', b'\r\n')
    replacement = replacement.replace(b'\n', b'\r\n')

if target not in content:
    print('ERROR: target not found!')
else:
    content = content.replace(target, replacement, 1)
    with open('/mnt/c/Antigravity/HEADRUSH/core/patch_pipeline.c', 'wb') as f:
        f.write(content)
    print('SUCCESS: patch_pipeline.c updated')
