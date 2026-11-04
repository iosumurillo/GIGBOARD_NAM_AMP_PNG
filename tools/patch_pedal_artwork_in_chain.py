#!/usr/bin/env python3
"""
patch_pedal_artwork_in_chain.py

Replaces generic colored pedal blocks in HeadRush signal chain (ActiveStomp.qml)
with authentic, detailed pedal artwork from ModuleEditors/img/<name>.png.
"""
import os
import sys
import zlib

TARGET_OFFSET_GIGBOARD = 0x1852310
TARGET_COMPRESSED_LEN = 2735
TARGET_UNCOMPRESSED_LEN = 15288

def verify_and_patch_evil(evil_data: bytearray) -> bool:
    pos = TARGET_OFFSET_GIGBOARD
    if pos + TARGET_COMPRESSED_LEN > len(evil_data):
        print(f"[-] Evil binary size {len(evil_data)} is too small for offset 0x{pos:x}", file=sys.stderr)
        return False

    prefix_uncomp = int.from_bytes(evil_data[pos-4:pos], "big")
    if prefix_uncomp != TARGET_UNCOMPRESSED_LEN:
        print(f"[-] Length prefix at 0x{pos-4:x} is {prefix_uncomp}, expected {TARGET_UNCOMPRESSED_LEN}", file=sys.stderr)
        return False

    orig_slice = bytes(evil_data[pos:pos+TARGET_COMPRESSED_LEN])
    if not orig_slice.startswith(b"\x78\x9c"):
        print(f"[-] Data at 0x{pos:x} is not a zlib stream", file=sys.stderr)
        return False

    # Decompress to verify it is indeed ActiveStomp.qml
    try:
        decomp = zlib.decompress(orig_slice)
        if b"FXModule_Active_3_PedalBody.png" not in decomp and b"ModuleEditors/img/" not in decomp:
            print("[-] Decompressed content at offset does not match ActiveStomp.qml signature", file=sys.stderr)
            return False
    except Exception as e:
        print(f"[-] Decompression error at 0x{pos:x}: {e}", file=sys.stderr)
        return False

    # Read our verified perfect patch
    patch_bin_path = os.path.join(os.path.dirname(__file__), "..", "scratch", "ActiveStomp_perfect_patch.bin")
    if not os.path.exists(patch_bin_path):
        patch_bin_path = os.path.join(os.path.dirname(__file__), "ActiveStomp_perfect_patch.bin")

    with open(patch_bin_path, "rb") as f:
        patch = f.read()

    assert len(patch) == TARGET_COMPRESSED_LEN, f"Patch size {len(patch)} != expected {TARGET_COMPRESSED_LEN}"

    # Apply patch
    evil_data[pos:pos+TARGET_COMPRESSED_LEN] = patch
    print(f"[+] Successfully patched ActiveStomp.qml @ 0x{pos:x} ({TARGET_COMPRESSED_LEN} bytes)")
    return True

def main():
    if len(sys.argv) < 2:
        evil_path = os.path.join("scratch", "Evil_gigboard")
        out_path = os.path.join("scratch", "Evil_gigboard_artwork_mod")
    else:
        evil_path = sys.argv[1]
        out_path = sys.argv[2] if len(sys.argv) > 2 else evil_path

    if not os.path.exists(evil_path):
        print(f"[-] Input file not found: {evil_path}", file=sys.stderr)
        sys.exit(1)

    with open(evil_path, "rb") as f:
        evil_data = bytearray(f.read())

    print(f"[*] Processing {evil_path} ({len(evil_data)} bytes)...")
    if not verify_and_patch_evil(evil_data):
        sys.exit(1)

    with open(out_path, "wb") as f:
        f.write(evil_data)

    print(f"[+] Output written to {out_path} ({len(evil_data)} bytes)")

if __name__ == "__main__":
    main()

