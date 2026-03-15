import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Show all unique tags and how many photos have each
c.execute("SELECT tags FROM images")
rows = c.fetchall()

tag_counts = {}
for row in rows:
    if row[0]:
        for tag in row[0].split(', '):
            tag = tag.strip()
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

# Sort by count
for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
    print(f'{tag}: {count} photos')

conn.close()