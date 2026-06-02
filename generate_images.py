import os
import django
from PIL import Image, ImageDraw, ImageFont

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Product

def create_placeholder_image(filename, text, color):
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Create an image with solid color
    img = Image.new('RGB', (400, 400), color=color)
    draw = ImageDraw.Draw(img)
    
    # Draw text in the center
    # We'll just draw some lines or simple text approximation since we don't have guaranteed fonts
    draw.text((100, 180), text, fill=(255, 255, 255))
    
    img.save(filename)
    return filename

def generate_images():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    media_dir = os.path.join(base_dir, 'media', 'products')
    
    # Create a default image
    create_placeholder_image(os.path.join(media_dir, 'default.png'), "No Image", "#95a5a6")
    
    # Create specific product images
    images = {
        'wireless-headphones': ('headphones.png', 'Headphones', '#2c3e50'),
        '4k-smart-tv': ('tv.png', '4K TV', '#e74c3c'),
        'python-crash-course': ('book.png', 'Python Book', '#27ae60'),
        'mens-tshirt': ('tshirt.png', 'T-Shirt', '#f39c12')
    }
    
    for slug, (filename, text, color) in images.items():
        filepath = os.path.join(media_dir, filename)
        create_placeholder_image(filepath, text, color)
        
        try:
            product = Product.objects.get(slug=slug)
            product.image = f'products/{filename}'
            product.save()
            print(f"Updated image for {slug}")
        except Product.DoesNotExist:
            print(f"Product {slug} not found.")

if __name__ == '__main__':
    generate_images()
    print("Images generated successfully!")
