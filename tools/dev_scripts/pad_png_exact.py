import zlib
import struct
from PIL import Image

TARGET_LEN = 75435

with open('/mnt/c/Antigravity/HEADRUSH/scratch/NAM_A2_pedal.png', 'rb') as f:
    png_data = f.read()

# Verify PNG signature
assert png_data.startswith(b'\x89PNG\r\n\x1a\n')

# Find IEND chunk
iend_idx = png_data.find(b'IEND')
assert iend_idx != -1
# IEND chunk starts 4 bytes before 'IEND' (its length field is 00 00 00 00)
iend_start = iend_idx - 4

# Everything before IEND:
head = png_data[:iend_start]
iend_chunk = png_data[iend_start:]

current_len = len(png_data)
diff = TARGET_LEN - current_len
print(f"Current len: {current_len}, Target: {TARGET_LEN}, Diff: {diff}")
assert diff >= 12, "PNG is already larger than target!"

# Chunk overhead is 4 (len) + 4 (type) + 4 (crc) = 12 bytes
payload_len = diff - 12
chunk_type = b'paDd'
payload = b'\x00' * payload_len

# Compute CRC over chunk_type + payload
crc = zlib.crc32(chunk_type + payload) & 0xffffffff

chunk = struct.pack('>I', payload_len) + chunk_type + payload + struct.pack('>I', crc)

padded_png = head + chunk + iend_chunk
print(f"New padded PNG length: {len(padded_png)} (Target: {TARGET_LEN})")
assert len(padded_png) == TARGET_LEN

out_path = '/mnt/c/Antigravity/HEADRUSH/scratch/NAM_A2_pedal_exact.png'
with open(out_path, 'wb') as f:
    f.write(padded_png)

# Verify with Pillow
im = Image.open(out_path)
im.verify()
print(f"Pillow verify PASSED: {im.format}, size={im.size}")

# Also reload and check getpixel
im2 = Image.open(out_path)
px = im2.getpixel((143, 221))
print("Center pixel test:", px)

