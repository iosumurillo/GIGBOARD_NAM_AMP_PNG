# We can run objdump from python in WSL to disassemble the jump targets
import subprocess

targets = [
    (0, "0x14de78"),
    (1, "0x14deac"),
    (2, "0x14e450"),
    (3, "0x14e5d0"),
    (4, "0x14e734"),
    (5, "0x14e750"),
    (6, "0x14e794"),
    (7, "0x14e7c0"),
    (8, "0x14e7ec"),
    (9, "0x14e854"),
    (10, "0x14d508"),
    (11, "0x14e8c8"),
    (12, "0x14e8d4"),
]

for idx, addr in targets:
    end_addr = hex(int(addr, 16) + 0x30)
    cmd = f"/opt/toolchain/bin/arm-buildroot-linux-gnueabihf-objdump -d --start-address={addr} --stop-address={end_addr} /mnt/c/Antigravity/HEADRUSH/scratch/Evil_gigboard"
    res = subprocess.run(["wsl", "-d", "Ubuntu", "bash", "-c", cmd], capture_output=True, text=True)
    lines = [l for l in res.stdout.splitlines() if "\t" in l][:6]
    print(f"=== Param {idx} ({addr}) ===")
    print("\n".join(lines))

