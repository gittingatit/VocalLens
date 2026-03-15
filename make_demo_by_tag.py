import sqlite3, os, shutil
from PIL import Image

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Tags we want to represent in the demo
target_tags = [
    'selfie', 'portrait', 'friends', 'outdoor', 'group of people',
    'flowers', 'night', 'people', 'sky', 'family',
    'smiling', 'sunset', 'dog', 'happy', 'wedding',
    'cat', 'rain', 'forest', 'food', 'graduation'
]

photos_per_tag = 10
dest = 'static/demo_samples'
os.makedirs(dest, exist_ok=True)

selected_paths = set()

for tag in target_tags:
    c.execute("SELECT path FROM images WHERE tags LIKE ? LIMIT ?", (f'%{tag}%', photos_per_tag))
    rows = c.fetchall()
    for row in rows:
        if row[0] and os.path.exists(row[0]):
            selected_paths.add(row[0])
    print(f'{tag}: {len(rows)} photos added')

conn.close()

print(f'\nTotal unique photos selected: {len(selected_paths)}')

# Copy and compress into demo_samples
copied = 0
for path in selected_paths:
    filename = os.path.basename(path)
    dest_path = os.path.join(dest, filename)
    try:
        img = Image.open(path).convert('RGB')
        img.thumbnail((1200, 1200), Image.LANCZOS)
        img.save(dest_path, 'JPEG', quality=75, optimize=True)
        copied += 1
    except Exception as e:
        print(f'Skipped {filename}: {e}')

# Final size
total = sum(
    os.path.getsize(os.path.join(r, f))
    for r, _, files in os.walk(dest)
    for f in files
)
print(f'Copied {copied} photos')
print(f'Total size: {total/1024/1024:.1f} MB')