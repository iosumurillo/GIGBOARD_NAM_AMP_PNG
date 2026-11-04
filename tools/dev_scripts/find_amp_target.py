with open('core/patch_pipeline.c', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'amp' in l.lower() and ('elf' in l.lower() or 'target' in l.lower() or 'vtable' in l.lower()):
        print(f'{i+1}: {l.strip()}')
        for j in range(max(0, i-2), min(len(lines), i+10)):
            print(f'  {j+1}: {lines[j]}', end='')

