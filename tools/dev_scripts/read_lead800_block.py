import sqlite3

conn = sqlite3.connect('firmware_rootfs/usr/Evil/Content/evil.db')
cursor = conn.cursor()
cursor.execute("SELECT name, content FROM blocks WHERE content LIKE '%82 LEAD 800%' OR content LIKE '%82 Lead 800%';")
rows = cursor.fetchall()
print(f"Found {len(rows)} blocks:")
for name, content in rows:
    print("Name:", name)
    print("Content:", content)

