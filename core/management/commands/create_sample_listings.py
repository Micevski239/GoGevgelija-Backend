from django.core.management.base import BaseCommand
from core.models import Listing

class Command(BaseCommand):
    help = 'Create sample listings for testing'

    def handle(self, *args, **options):
        sample_listings = [
            {
                'title': 'Balkan Bistro',
                'rating': 4.7,
                'address': 'Central Square, Gevgelija',
                'open_time': 'Open until 23:00',
                'category': 'restaurant',
                'tags': ['Grill', 'Family', 'Outdoor'],
                'image': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=1974&auto=format&fit=crop',
                'featured': True
            },
            {
                'title': 'Villa Rose Restaurant',
                'rating': 4.8,
                'address': 'Old Town, Gevgelija',
                'open_time': 'Open until 22:30',
                'category': 'restaurant',
                'tags': ['Fine Dining', 'Romantic', 'Wine'],
                'image': 'https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=2070&auto=format&fit=crop',
                'featured': True
            },
            {
                'title': 'Coffee Corner',
                'rating': 4.5,
                'address': 'Main Street 15, Gevgelija',
                'open_time': 'Open until 20:00',
                'category': 'cafe',
                'tags': ['Coffee', 'Pastries', 'WiFi'],
                'image': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=2069&auto=format&fit=crop',
                'featured': True
            },
            {
                'title': 'Garden Grill',
                'rating': 4.6,
                'address': 'Park Avenue 8, Gevgelija',
                'open_time': 'Open until 24:00',
                'category': 'restaurant',
                'tags': ['BBQ', 'Garden', 'Live Music'],
                'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?q=80&w=2071&auto=format&fit=crop',
                'featured': True
            },
            {
                'title': 'Sweet Dreams Bakery',
                'rating': 4.3,
                'address': 'Liberty Street 22, Gevgelija',
                'open_time': 'Open until 18:00',
                'category': 'cafe',
                'tags': ['Bakery', 'Sweets', 'Fresh Bread'],
                'image': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?q=80&w=2070&auto=format&fit=crop',
                'featured': False
            },
            {
                'title': 'Night Owl Bar',
                'rating': 4.4,
                'address': 'Downtown District, Gevgelija',
                'open_time': 'Open until 02:00',
                'category': 'bar',
                'tags': ['Cocktails', 'Late Night', 'Music'],
                'image': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?q=80&w=2070&auto=format&fit=crop',
                'featured': False
            }
        ]

        for listing_data in sample_listings:
            listing, created = Listing.objects.get_or_create(
                title=listing_data['title'],
                defaults=listing_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created listing "{listing.title}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Listing "{listing.title}" already exists')
                )

        self.stdout.write(
            self.style.SUCCESS('Sample listings creation completed!')
        )