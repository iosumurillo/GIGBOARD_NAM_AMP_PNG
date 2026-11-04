from PIL import Image

im234 = Image.open('/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/img_234_0x02180c1a.png')
im235 = Image.open('/mnt/c/Antigravity/HEADRUSH/scratch/extracted_pngs/img_235_0x02190255.png')

print(f"img_234: size={im234.size}")
print(f"img_235: size={im235.size}")

# Let's save both as readable files in brain directory so we can inspect them!
im234.save('/mnt/c/Users/iosum/.gemini/antigravity/brain/2a216885-5d34-42c0-8d6a-137f7c23b39f/pedal_234.png')
im235.save('/mnt/c/Users/iosum/.gemini/antigravity/brain/2a216885-5d34-42c0-8d6a-137f7c23b39f/pedal_235.png')
print("Saved pedal_234.png and pedal_235.png to brain directory!")

