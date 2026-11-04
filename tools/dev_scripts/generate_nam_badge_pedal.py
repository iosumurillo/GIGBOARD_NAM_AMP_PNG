import zlib
import struct
from PIL import Image, ImageDraw, ImageFont

def make_nam_image(width, height, chassis_rect, radius, font_size, out_path):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    x0, y0, x1, y1 = chassis_rect

    # Sleek dark drop shadow
    for s in range(4, 0, -1):
        draw.rounded_rectangle([x0 - s, y0 - s + 2, x1 + s, y1 + s + 3], radius=radius + s, fill=(0, 0, 0, int(30 / s)))

    # Pure black pedal body / badge
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=(0, 0, 0, 255), outline=(35, 35, 38, 255), width=2)

    # White text "NAM" in bold capital letters
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.text((cx, cy), "NAM", fill=(255, 255, 255, 255), font=font, anchor="mm")

    img.save(out_path, format="PNG")
    print(f"Saved {out_path} ({width}x{height})")

def pad_png(src_path, dst_path, target_len):
    with open(src_path, 'rb') as f:
        data = f.read()
    assert data.startswith(b'\x89PNG\r\n\x1a\n')
    iend_idx = data.find(b'IEND')
    assert iend_idx != -1
    iend_start = iend_idx - 4
    head = data[:iend_start]
    iend_chunk = data[iend_start:]

    diff = target_len - len(data)
    assert diff >= 12, f"Image {len(data)} too large for target {target_len}"

    payload_len = diff - 12
    chunk_type = b'paDd'
    payload = b'\x00' * payload_len
    crc = zlib.crc32(chunk_type + payload) & 0xffffffff
    chunk = struct.pack('>I', payload_len) + chunk_type + payload + struct.pack('>I', crc)

    padded = head + chunk + iend_chunk
    assert len(padded) == target_len, f"Padded {len(padded)} != {target_len}"
    with open(dst_path, 'wb') as f:
        f.write(padded)
    print(f"Padded {dst_path} to {len(padded)} bytes (exact target: {target_len})")

if __name__ == '__main__':
    # V1: 286 x 442, target 75435
    v1_raw = 'scratch/nam_badge_v1.png'
    v1_exact = 'scratch/nam_badge_v1_exact.png'
    make_nam_image(286, 442, (33, 29, 253, 415), 16, 76, v1_raw)
    pad_png(v1_raw, v1_exact, 75435)

    # V2: 286 x 436, target 63031
    v2_raw = 'scratch/nam_badge_v2.png'
    v2_exact = 'scratch/nam_badge_v2_exact.png'
    make_nam_image(286, 436, (50, 30, 236, 408), 16, 72, v2_raw)
    pad_png(v2_raw, v2_exact, 63031)

    print("SUCCESS: Both images generated and padded!")

