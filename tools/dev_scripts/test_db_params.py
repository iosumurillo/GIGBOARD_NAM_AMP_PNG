import sqlite3, json

conn = sqlite3.connect('firmware_rootfs/usr/Evil/Content/evil.db')
c = conn.cursor()
c.execute("SELECT name, content FROM blocks WHERE name LIKE '%82 LEAD 800 BRIGHT%';")
row = c.fetchone()
data = json.loads(row[1])
print(json.dumps(data, indent=2))

