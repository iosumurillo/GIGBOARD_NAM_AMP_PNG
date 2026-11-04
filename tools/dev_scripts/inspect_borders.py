from PIL import Image

p_amp = r'C:/Users/iosum/.gemini/antigravity/brain/47acffb5-1b93-4f9a-be37-e545b83d88e3/.user_uploaded/media_1793778228977_4abc4965.jpg'
p_pedal = r'C:/Users/iosum/.gemini/antigravity/brain/47acffb5-1b93-4f9a-be37-e545b83d88e3/.user_uploaded/media_1793778228916_c38d5f47.jpg'

im_amp = Image.open(p_amp)
im_pedal = Image.open(p_pedal)

# Let's inspect the borders of im_amp and im_pedal
print('Amp borders: top middle=', im_amp.getpixel((im_amp.width//2, 2)),
      'bottom middle=', im_amp.getpixel((im_amp.width//2, im_amp.height-3)),
      'left middle=', im_amp.getpixel((2, im_amp.height//2)),
      'right middle=', im_amp.getpixel((im_amp.width-3, im_amp.height//2)))

print('Pedal borders: top middle=', im_pedal.getpixel((im_pedal.width//2, 2)),
      'bottom middle=', im_pedal.getpixel((im_pedal.width//2, im_pedal.height-3)),
      'left middle=', im_pedal.getpixel((2, im_pedal.height//2)),
      'right middle=', im_pedal.getpixel((im_pedal.width-3, im_pedal.height//2)))

