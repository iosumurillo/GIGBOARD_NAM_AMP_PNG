with open('core/launcher_script.c', 'r') as f:
    text = f.read()

# Let's see what line 150-165 looks like
for line in text.splitlines()[150:165]:
    print(line)

