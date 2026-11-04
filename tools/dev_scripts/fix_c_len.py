with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'r', encoding='utf-8') as f:
    text = f.read()

# Add one \n at the end of new_text so it matches exactly 420 chars
text = text.replace('\\n\\n\\n\\n\\n\\n\\n"}', '\\n\\n\\n\\n\\n\\n\\n\\n"}')

with open('c:/Antigravity/HEADRUSH/core/model_targets.c', 'w', encoding='utf-8') as f:
    f.write(text)

print("model_targets.c updated with exact length match")

