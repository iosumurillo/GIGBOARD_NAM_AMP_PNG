with open('core/elf_patch.c', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'amp' in l.lower():
        print(f'{i+1}: {l.strip()}')

