"""
Image Helper Module - Handle product images
"""
import os
import shutil
from tkinter import filedialog
from PIL import Image, ImageTk

# Image directory
IMAGE_DIR = "product_images"
DEFAULT_IMAGE = os.path.join(IMAGE_DIR, "default.png")

def ensure_image_directory():
    """Create image directory if it doesn't exist"""
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print(f"Created directory: {IMAGE_DIR}")

def browse_image():
    """Open file dialog to select an image"""
    filename = filedialog.askopenfilename(
        title="Select Product Image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
    )
    return filename

def save_product_image(source_path, product_name):
    """Copy image to product_images folder with proper naming"""
    if not source_path or not os.path.exists(source_path):
        print(f"Error: Source image not found: {source_path}")
        return None
    
    ensure_image_directory()
    
    # If the image is already in the product_images folder, just return the filename
    if os.path.dirname(os.path.abspath(source_path)) == os.path.abspath(IMAGE_DIR):
        return os.path.basename(source_path)
    
    # Get file extension (handle double extensions like .jpg.webp)
    filename = os.path.basename(source_path)
    name_parts = filename.split('.')
    if len(name_parts) > 1:
        # Keep all extensions (e.g., .jpg.webp)
        ext = '.' + '.'.join(name_parts[1:])
    else:
        ext = ''
    
    # Create safe filename
    safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')
    
    # Create destination path
    dest_filename = f"{safe_name}{ext}"
    dest_path = os.path.join(IMAGE_DIR, dest_filename)
    
    # Handle duplicate filenames
    counter = 1
    while os.path.exists(dest_path):
        dest_filename = f"{safe_name}_{counter}{ext}"
        dest_path = os.path.join(IMAGE_DIR, dest_filename)
        counter += 1
    
    try:
        shutil.copy2(source_path, dest_path)
        print(f"✓ Image copied: {source_path} -> {dest_filename}")
        return dest_filename  # Return relative path
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

def load_image_for_display(image_path, size=(100, 100)):
    """Load and resize image for tkinter display"""
    try:
        # Try multiple path options
        paths_to_try = []
        
        if image_path:
            # Try as absolute path
            paths_to_try.append(image_path)
            # Try as relative path from IMAGE_DIR
            paths_to_try.append(os.path.join(IMAGE_DIR, image_path))
            # Try just the filename
            if os.path.basename(image_path) != image_path:
                paths_to_try.append(os.path.join(IMAGE_DIR, os.path.basename(image_path)))
        
        img = None
        for path in paths_to_try:
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    break
                except Exception as e:
                    print(f"Failed to open {path}: {e}")
                    continue
        
        if img is None:
            # Return placeholder
            print(f"Could not load image: {image_path}, using placeholder")
            img = Image.new('RGB', size, color='#E0E0E0')
        
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        # Return placeholder
        img = Image.new('RGB', size, color='#E0E0E0')
        return ImageTk.PhotoImage(img)

def get_image_path(filename):
    """Get full path to image file"""
    if not filename:
        return None
    return os.path.join(IMAGE_DIR, filename)

def delete_product_image(filename):
    """Delete product image file"""
    if not filename:
        return
    
    path = os.path.join(IMAGE_DIR, filename)
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted image: {filename}")
    except Exception as e:
        print(f"Error deleting image: {e}")
