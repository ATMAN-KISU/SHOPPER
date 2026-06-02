import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product
from django.contrib.auth.models import User

def populate():
    # Create superuser if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created: admin / admin123")

    # Categories
    categories = [
        {'title': 'Electronics', 'slug': 'electronics'},
        {'title': 'Books', 'slug': 'books'},
        {'title': 'Clothing', 'slug': 'clothing'},
    ]
    
    for cat_data in categories:
        Category.objects.get_or_create(title=cat_data['title'], slug=cat_data['slug'])

    # Products
    elec = Category.objects.get(slug='electronics')
    books = Category.objects.get(slug='books')
    clothing = Category.objects.get(slug='clothing')

    products = [
        {
            'title': 'Wireless Noise Cancelling Headphones',
            'slug': 'wireless-headphones',
            'description': 'Premium noise cancelling headphones with 30-hour battery life.',
            'price': 299.99,
            'discount_price': 249.99,
            'category': elec,
        },
        {
            'title': '4K Ultra HD Smart TV',
            'slug': '4k-smart-tv',
            'description': '55-inch 4K Smart TV with built-in streaming apps.',
            'price': 599.99,
            'category': elec,
        },
        {
            'title': 'The Python Crash Course',
            'slug': 'python-crash-course',
            'description': 'A hands-on, project-based introduction to programming.',
            'price': 39.95,
            'category': books,
        },
        {
            'title': 'Men\'s Casual T-Shirt',
            'slug': 'mens-tshirt',
            'description': 'Comfortable 100% cotton casual t-shirt.',
            'price': 19.99,
            'discount_price': 14.99,
            'category': clothing,
        }
    ]

    for prod_data in products:
        Product.objects.get_or_create(
            slug=prod_data['slug'],
            defaults=prod_data
        )
    print("Database populated with sample data!")

if __name__ == '__main__':
    populate()
