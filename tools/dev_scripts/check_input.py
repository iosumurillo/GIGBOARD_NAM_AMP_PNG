import json

with open(r'C:\Users\iosum\.gemini\antigravity\brain\47acffb5-1b93-4f9a-be37-e545b83d88e3\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('type') == 'USER_INPUT':
            last_user = data

print('step_index:', last_user.get('step_index'))
print('keys:', list(last_user.keys()))
print('content:', repr(last_user.get('content')))
print('media:', last_user.get('media'))

