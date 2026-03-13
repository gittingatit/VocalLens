"""
One-time script to download images from Google Drive
Run this after cloning the repository
"""

import gdown
import os
from pathlib import Path

# Your Google Drive folder ID (just the ID, not the full URL)
FOLDER_ID = "1angvCg8NK3JDgJqUIQJmBs6558y5FOnE"

def download_images():
    """Download all images from Google Drive folder"""
    
    print("=" * 60)
    print("📸 VOCAL LENS - Image Dataset Downloader")
    print("=" * 60)
    
    # Create samples folder
    samples_path = Path("static/samples")
    samples_path.mkdir(parents=True, exist_ok=True)
    
    # Check if images already exist
    existing_images = list(samples_path.glob("*.jpg")) + list(samples_path.glob("*.jpeg")) + list(samples_path.glob("*.png"))
    if existing_images:
        print(f"✅ Found {len(existing_images)} existing images in static/samples/")
        overwrite = input("Download again? (y/n): ").lower()
        if overwrite != 'y':
            print("Skipping download.")
            return
    
    # Download using folder ID (this is the fixed part)
    print(f"\n📥 Downloading images using folder ID: {FOLDER_ID}")
    print(f"   This may take a few minutes depending on your internet speed.\n")
    
    try:
        # USE THIS LINE - it's the fix!
        gdown.download_folder(
            id=FOLDER_ID,  # Using 'id=' instead of full URL
            output=str(samples_path),
            quiet=False,
            remaining_ok=True
        )
        
        print(f"\n✅ Download complete! Images saved to: {samples_path}")
        
        # Count downloaded images
        images = list(samples_path.glob("*.jpg")) + list(samples_path.glob("*.jpeg")) + list(samples_path.glob("*.png"))
        print(f"📊 Total images: {len(images)}")
        
    except Exception as e:
        print(f"\n❌ Error downloading: {e}")
        print("\n💡 Alternative: Download manually from Google Drive and extract to static/samples/")
        print(f"   Folder URL: https://drive.google.com/drive/folders/{FOLDER_ID}")

if __name__ == "__main__":
    download_images()