import sqlite3

conn = sqlite3.connect('firmware_rootfs/usr/Evil/Content/evil.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cursor.fetchall()]
print("Tables in evil.db:", tables)

for t in tables:
    cursor.execute(f"PRAGMA table_info({t});")
    cols = [c[1] for c in cursor.fetchall()]
    print(f"Table {t}: {cols}")
    cursor.execute(f"SELECT * FROM {t} WHERE 1 LIMIT 3;")
    print("  Samples:", cursor.fetchall()[:2])

