with open('C:/Antigravity/HEADRUSH/scratch/Evil_gigboard', 'rb') as f:
    # 0x13a0a0 is code in .text (vaddr = off + 0x8000)
    file_off = 0x13a0a0 - 0x8000
    f.seek(file_off)
    code = f.read(500)

import capstone
md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
for i in md.disasm(code, 0x13a0a0):
    print(f"0x{i.address:x}: {i.mnemonic} {i.op_str}")

