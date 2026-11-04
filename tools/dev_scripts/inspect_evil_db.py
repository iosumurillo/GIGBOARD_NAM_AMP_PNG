import sqlite3, json

db_path = 'firmware_rootfs/usr/Evil/Content/evil.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT id, type, name, content FROM blocks WHERE type LIKE '%82%' OR name LIKE '%82%' OR type LIKE '%LEAD%' OR name LIKE '%LEAD%';")
rows = cur.fetchall()
print(f'Found {len(rows)} matching blocks:')
for r in rows:
    print(f'ID: {r[0]} | Type: {r[1]} | Name: {r[2]}')
    parsed = json.loads(r[3])
    print(json.dumps(parsed, indent=2))
    print('='*50)


