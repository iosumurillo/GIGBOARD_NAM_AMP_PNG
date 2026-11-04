import os

def bin2c(in_path, out_path, sym_name):
    with open(in_path, 'rb') as f:
        data = f.read()
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"/* generated from {in_path} */\n")
        f.write(f"const unsigned char {sym_name}[] = {{\n")
        for i, b in enumerate(data):
            f.write(f"0x{b:02x},")
            if (i + 1) % 16 == 0:
                f.write("\n")
        f.write("\n};\n")
        f.write(f"const unsigned long {sym_name}_len = {len(data)}UL;\n")
    print(f"Generated {out_path} ({len(data)} bytes, symbol {sym_name})")

os.makedirs('c:/Antigravity/HEADRUSH/core/generated', exist_ok=True)
bin2c('c:/Antigravity/HEADRUSH/blobs/libnam_hook.so', 'c:/Antigravity/HEADRUSH/core/generated/blob_nam_hook.c', 'g_nam_hook_so')
bin2c('c:/Antigravity/HEADRUSH/blobs/libnam_preload.so', 'c:/Antigravity/HEADRUSH/core/generated/blob_nam_preload.c', 'g_nam_preload_so')
bin2c('c:/Antigravity/HEADRUSH/blobs/trampoline_gonk.bin', 'c:/Antigravity/HEADRUSH/core/generated/blob_trampoline_gonk.c', 'g_nam_trampoline_gonk_bin')
print("All blob sources generated successfully!")

