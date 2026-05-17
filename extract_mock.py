import sqlite3, json

conn = sqlite3.connect('takhleeqx.db')
conn.row_factory = sqlite3.Row
row = conn.execute('SELECT * FROM campaigns LIMIT 1').fetchone()
if row:
    d = dict(row)
    d.pop('id', None)
    d.pop('restaurant_id', None)
    with open('backend/mock_campaign.json', 'w') as f:
        json.dump(d, f)
    print("Mock campaign saved.")
else:
    print("No campaigns found.")
