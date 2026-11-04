import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Target dimensions: 286 x 442, RGBA
WIDTH = 286
HEIGHT = 442

img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 1. Enclosure background with rounded corners
# Outer chassis bounds
pad_x = 14
pad_top = 16
pad_bot = 16
x0, y0 = pad_x, pad_top
x1, y1 = WIDTH - pad_x, HEIGHT - pad_bot
radius = 20

# Drop shadow under pedal
for s in range(6, 0, -1):
    shadow_alpha = int(40 / s)
    draw.rounded_rectangle([x0 - s, y0 - s + 4, x1 + s, y1 + s + 6], radius=radius + s, fill=(0, 0, 0, shadow_alpha))

# Chassis base: sleek brushed dark slate / graphite metallic gradient
base_chassis = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
base_draw = ImageDraw.Draw(base_chassis)
base_draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=(35, 38, 44, 255))

# Vertical gradient on chassis
for y in range(y0, y1):
    factor = (y - y0) / (y1 - y0)
    # subtle top-to-bottom metallic gradient
    # Top is slightly lighter slate, bottom is darker graphite
    r = int(42 * (1 - factor * 0.4) + 18 * factor)
    g = int(46 * (1 - factor * 0.4) + 20 * factor)
    b = int(54 * (1 - factor * 0.4) + 26 * factor)
    # Draw line clipped to chassis mask
    for x in range(x0, x1):
        if base_chassis.getpixel((x, y))[3] > 0:
            base_chassis.putpixel((x, y), (r, g, b, 255))

img = Image.alpha_composite(img, base_chassis)
draw = ImageDraw.Draw(img)

# Metallic beveled border (outer silver/cyan accent trim)
draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=(80, 95, 110, 255), width=2)
draw.rounded_rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], radius=radius - 2, outline=(25, 28, 32, 255), width=1)
# Top inner highlight line
draw.line([x0 + radius, y0 + 3, x1 - radius, y0 + 3], fill=(120, 140, 160, 180), width=1)

# Inner recessed faceplate (anodized black / deep midnight with subtle cyan/teal border)
fx0, fy0 = x0 + 10, y0 + 12
fx1, fy1 = x1 - 10, y1 - 12
face_radius = 12
draw.rounded_rectangle([fx0, fy0, fx1, fy1], radius=face_radius, fill=(20, 22, 26, 255), outline=(0, 190, 220, 160), width=2)

# Subtle decorative corner screws (hex bolts)
screws = [(fx0 + 8, fy0 + 8), (fx1 - 8, fy0 + 8), (fx0 + 8, fy1 - 8), (fx1 - 8, fy1 - 8)]
for sx, sy in screws:
    draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(70, 75, 82, 255), outline=(130, 135, 145, 255))
    draw.line([sx - 3, sy, sx + 3, sy], fill=(30, 32, 35, 255), width=1)

# Helper function to draw a 3D knurled metal knob with indicator
def draw_knob(center_x, center_y, outer_r, label, value_angle_deg=-45):
    # Knob drop shadow
    draw.ellipse([center_x - outer_r - 2, center_y - outer_r, center_x + outer_r + 2, center_y + outer_r + 4], fill=(0, 0, 0, 140))
    # Outer notched rim
    draw.ellipse([center_x - outer_r, center_y - outer_r, center_x + outer_r, center_y + outer_r], fill=(50, 53, 58, 255), outline=(90, 95, 105, 255), width=2)
    # Inner knob face (brushed dark metal)
    inner_r = outer_r - 4
    draw.ellipse([center_x - inner_r, center_y - inner_r, center_x + inner_r, center_y + inner_r], fill=(28, 30, 34, 255), outline=(140, 150, 165, 255), width=1)
    # Center cap
    cap_r = inner_r - 6
    draw.ellipse([center_x - cap_r, center_y - cap_r, center_x + cap_r, center_y + cap_r], fill=(40, 44, 50, 255))
    
    # White indicator notch
    rad = math.radians(value_angle_deg)
    nx1 = center_x + int((cap_r - 1) * math.cos(rad))
    ny1 = center_y + int((cap_r - 1) * math.sin(rad))
    nx2 = center_x + int((inner_r - 1) * math.cos(rad))
    ny2 = center_y + int((inner_r - 1) * math.sin(rad))
    draw.line([nx1, ny1, nx2, ny2], fill=(255, 255, 255, 255), width=2)
    
    # Knob Label
    draw.text((center_x, center_y + outer_r + 5), label, fill=(180, 190, 205, 255), anchor="mt")

# Load nice TTF fonts if available, or default
try:
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    font_knob = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_knob = ImageFont.load_default()

# 2. Draw 3 Knobs at the top
# DRIVE (left), TONE (right), LEVEL (center)
draw_knob(WIDTH // 2 - 62, 70, 26, "DRIVE", -135)
draw_knob(WIDTH // 2 + 62, 70, 26, "TONE", 45)
draw_knob(WIDTH // 2, 138, 26, "LEVEL", 0)

# 3. LED Indicator
led_x = WIDTH // 2
led_y = 186
# Chrome bezel
draw.ellipse([led_x - 8, led_y - 8, led_x + 8, led_y + 8], fill=(90, 95, 105, 255), outline=(160, 170, 180, 255), width=1)
# Glowing Cyan/Teal LED
draw.ellipse([led_x - 5, led_y - 5, led_x + 5, led_y + 5], fill=(0, 220, 255, 255))
draw.ellipse([led_x - 2, led_y - 2, led_x + 2, led_y + 2], fill=(220, 255, 255, 255))

# 4. Big Bold Branding: "NAM A2"
# Background badge panel for the logo
badge_y0 = 212
badge_y1 = 306
draw.rounded_rectangle([fx0 + 12, badge_y0, fx1 - 12, badge_y1], radius=8, fill=(14, 15, 18, 255), outline=(40, 50, 60, 255), width=1)

# Subtle accent stripes
draw.line([fx0 + 20, badge_y0 + 2, fx1 - 20, badge_y0 + 2], fill=(0, 180, 220, 200), width=2)
draw.line([fx0 + 20, badge_y1 - 2, fx1 - 20, badge_y1 - 2], fill=(0, 180, 220, 200), width=2)

# Text "NAM" in huge modern bold typography
# Cyan / white glowing text
draw.text((WIDTH // 2, 222), "NAM", fill=(255, 255, 255, 255), font=font_title, anchor="mt")
# Text "A2" in high-contrast electric cyan
draw.text((WIDTH // 2, 268), "A2", fill=(0, 215, 255, 255), font=font_sub, anchor="mt")

# Subtitle under badge
draw.text((WIDTH // 2, 318), "NEURAL AMP MODELER", fill=(140, 155, 170, 255), font=font_small, anchor="mt")

# 5. Heavy-Duty 3D Metallic Footswitch
switch_cx = WIDTH // 2
switch_cy = 372
# Hex Nut Base
nut_r = 24
nut_points = []
for i in range(6):
    angle = math.radians(i * 60 + 30)
    nut_points.append((switch_cx + int(nut_r * math.cos(angle)), switch_cy + int(nut_r * math.sin(angle))))
draw.polygon(nut_points, fill=(90, 95, 105, 255), outline=(160, 170, 180, 255))

# Inner chrome ring
draw.ellipse([switch_cx - 16, switch_cy - 16, switch_cx + 16, switch_cy + 16], fill=(130, 135, 145, 255), outline=(190, 200, 210, 255), width=1)
# Center plunger (brushed silver)
draw.ellipse([switch_cx - 12, switch_cy - 12, switch_cx + 12, switch_cy + 12], fill=(180, 185, 195, 255), outline=(220, 230, 240, 255), width=2)
draw.ellipse([switch_cx - 6, switch_cy - 6, switch_cx + 6, switch_cy + 6], fill=(220, 225, 235, 255))

# Save image
out_path = "/mnt/c/Antigravity/HEADRUSH/scratch/NAM_A2_pedal.png"
img.save(out_path, format="PNG")
print(f"Generated {out_path} ({WIDTH}x{HEIGHT}) successfully!")

