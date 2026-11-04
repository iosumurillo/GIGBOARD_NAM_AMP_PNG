import sys, struct, lzma

with open('scratch/Update_patched.img', 'rb') as f:
    fit_data = f.read()

print('FIT size:', len(fit_data))

# Find rootfs node in FIT
# We can decompress rootfs from FIT
# Let's find the XZ header in FIT data
# XZ magic: 0xFD, '7', 'z', 'X', 'Z', 0x00
xz_magic = b'\xfd7zXZ\x00'
offsets = []
pos = 0
while True:
    idx = fit_data.find(xz_magic, pos)
    if idx == -1: break
    offsets.append(idx)
    pos = idx + 1

print('Found XZ streams at offsets:', offsets)
# Decompress each
for i, off in enumerate(offsets):
    try:
        decomp = lzma.decompress(fit_data[off:off+60*1024*1024])
        print(f'Stream {i} at offset {off}: decompressed size {len(decomp)}')
        # Check if ext4
        # Check for /usr/Evil/Scripts/evil
        idx_evil = decomp.find(b'systemd-inhibit --what=handle-power-key')
        if idx_evil != -1:
            print(f'Found launcher line in stream {i}:')
            print(decomp[idx_evil:idx_evil+250].decode(errors='replace'))
        idx_badge = decomp.find(b'82 LEAD 800 (NAM)')
        if idx_badge != -1:
            print(f'Found 82 LEAD 800 (NAM) in stream {i} at {idx_badge}')
        idx_slot = decomp.find(b'NAM_HOOK_SLOT_AMP_ADDR')
        if idx_slot != -1:
            print(f'Found NAM_HOOK_SLOT_AMP_ADDR in stream {i} at {idx_slot}')
    except Exception as e:
        print(f'Stream {i} error: {e}')

