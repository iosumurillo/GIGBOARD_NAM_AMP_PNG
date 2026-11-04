from PIL import Image

p_amp = r'C:/Users/iosum/.gemini/antigravity/brain/47acffb5-1b93-4f9a-be37-e545b83d88e3/.user_uploaded/media_1793778228977_4abc4965.jpg'
p_pedal = r'C:/Users/iosum/.gemini/antigravity/brain/47acffb5-1b93-4f9a-be37-e545b83d88e3/.user_uploaded/media_1793778228916_c38d5f47.jpg'

im_amp = Image.open(p_amp)
im_pedal = Image.open(p_pedal)

print('Amp image:', im_amp.size, im_amp.format, im_amp.mode)
print('Pedal image:', im_pedal.size, im_pedal.format, im_pedal.mode)

# Check corner colors:
print('Amp corners:', [im_amp.getpixel((x, y)) for x, y in [(0, 0), (im_amp.width-1, 0), (0, im_amp.height-1), (im_amp.width-1, im_amp.height-1)]])
print('Pedal corners:', [im_pedal.getpixel((x, y)) for x, y in [(0, 0), (im_pedal.width-1, 0), (0, im_pedal.height-1), (im_pedal.width-1, im_pedal.height-1)]])

