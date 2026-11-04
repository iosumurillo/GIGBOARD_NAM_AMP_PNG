import sqlite3
conn = sqlite3.connect('scratch/evil.db')
cur = conn.cursor()
types = cur.execute("SELECT DISTINCT type FROM blocks").fetchall()
print('Distinct block types in evil.db:')
for t in types:
    print(t[0])
