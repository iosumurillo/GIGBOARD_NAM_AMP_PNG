import os
import shutil
import struct
import subprocess

print("--- Starting Repack ---")

STOCK_EXE = r"c:\Antigravity\HEADRUSH\release\HeadRush gigboard Firmware Updater (stock).exe"
PATCHED_IMG = r"c:\Antigravity\HEADRUSH\scratch\Update_patched.img"
OUT_EXE = r"c:\Antigravity\HEADRUSH\release\HeadRush gigboard Firmware Updater (NAM mod).exe"
SEVENZIP = r"c:\Antigravity\HEADRUSH\release\7z.exe"
WORKDIR = r"c:\Antigravity\HEADRUSH\scratch\repack_work"

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# 1. Read stock exe and extract SFX prefix
with open(STOCK_EXE, "rb") as f:
    stock_data = f.read()

sfx_marker = b";!@InstallEnd@!"
marker_idx = stock_data.find(sfx_marker)
assert marker_idx != -1, "SFX marker not found"
archive_start = marker_idx + len(sfx_marker)

sfx_prefix = bytearray(stock_data[:archive_start])

# Strip Authenticode Security directory from PE header
e_lfanew = struct.unpack('<I', sfx_prefix[0x3c:0x40])[0]
assert sfx_prefix[e_lfanew:e_lfanew+4] == b"PE\x00\x00", "PE signature mismatch"
coff_off = e_lfanew + 4
opt_off = coff_off + 20
magic = struct.unpack('<H', sfx_prefix[opt_off:opt_off+2])[0]
assert magic == 0x10b, f"PE32 magic mismatch: {magic:#x}"
numrva_off = opt_off + 92
sec_entry_off = numrva_off + 4 + 4 * 8
sfx_prefix[sec_entry_off:sec_entry_off+8] = b'\x00' * 8
print("Stripped Authenticode from SFX prefix.")

# 2. Extract payload files from stock exe
payload_dir = os.path.join(WORKDIR, "payload")
os.makedirs(payload_dir, exist_ok=True)

# Save embedded stock 7z
stock_7z = os.path.join(WORKDIR, "stock.7z")
with open(stock_7z, "wb") as f:
    f.write(stock_data[archive_start:])

subprocess.run([SEVENZIP, "x", f"-o{payload_dir}", stock_7z, "-y"], check=True)
print("Extracted stock payload.")

# Replace Update.img with our patched image
shutil.copyfile(PATCHED_IMG, os.path.join(payload_dir, "Update.img"))
print(f"Copied {PATCHED_IMG} -> payload/Update.img ({os.path.getsize(PATCHED_IMG)} bytes)")

# 3. Create new 7z archive in exact order
entries = ["Background.png", "Config.json", "FirmwareUpdater.exe", "Update.img", "libusb-1.0.dll"]
new_7z = os.path.join(WORKDIR, "new.7z")

cmd = [SEVENZIP, "a", new_7z] + entries
subprocess.run(cmd, cwd=payload_dir, check=True)
print("Created new.7z archive.")

# 4. Concatenate sfx_prefix + new_7z -> OUT_EXE
with open(new_7z, "rb") as f:
    new_7z_data = f.read()

with open(OUT_EXE, "wb") as f:
    f.write(sfx_prefix)
    f.write(new_7z_data)

print(f"Wrote {OUT_EXE} ({os.path.getsize(OUT_EXE)} bytes)")

# 5. Verify integrity with 7z test
res = subprocess.run([SEVENZIP, "t", OUT_EXE], capture_output=True, text=True)
print("7z test output:\n", res.stdout)
assert "Everything is Ok" in res.stdout, "7z test failed!"
print("SUCCESS! Repacked updater verified 100% OK!")

