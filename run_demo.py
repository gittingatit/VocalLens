import os
import shutil
from PIL import Image

source = 'static/samples'
dest = 'static/demo_samples'
photos_per_folder = 15
max_size_kb = 200

os.makedirs(dest, exist_ok=True)

for folder in os.listdir(source):
    src_folder = os.path.join(source, folder)
    if not os.path.isdir(src_folder):
        continue

    # Collect all images recursively
    all_images = []
    for root, dirs, files in os.walk(src_folder):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                all_images.append(os.path.join(root, f))

    # Sort by file size ascending (smaller = already compressed = faster)
    all_images.sort(key=lambda x: os.path.getsize(x))

    # Take the first N
    selected = all_images[:photos_per_folder]

    dest_folder = os.path.join(dest, folder)
    os.makedirs(dest_folder, exist_ok=True)

    for img_path in selected:
        filename = os.path.basename(img_path)
        dest_path = os.path.join(dest_folder, filename)

        try:
            img = Image.open(img_path).convert('RGB')
            # Resize if too large
            img.thumbnail((1200, 1200), Image.LANCZOS)
            # Save with compression
            quality = 75
            img.save(dest_path, 'JPEG', quality=quality, optimize=True)
            size_kb = os.path.getsize(dest_path) / 1024
            print(f'  {filename}: {size_kb:.0f}KB')
        except Exception as e:
            print(f'  Skipped {filename}: {e}')

    print(f'Done: {folder} — {len(selected)} photos')

# Final size check
total = sum(
    os.path.getsize(os.path.join(r, f))
    for r, _, files in os.walk(dest)
    for f in files
)
print(f'\nTotal demo_samples size: {total/1024/1024:.1f} MB')