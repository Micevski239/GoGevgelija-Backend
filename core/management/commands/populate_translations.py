from django.core.management.base import BaseCommand
from core.models import Listing, Event, Category, Promotion, Blog

class Command(BaseCommand):
    help = 'Populate sample translations for existing content'

    def handle(self, *args, **options):
        # Update Categories
        categories_translations = {
            'Restaurants': 'Ресторани',
            'Cafes': 'Кафеани', 
            'Hotels': 'Хотели',
            'Attractions': 'Атракции',
            'Shopping': 'Шопинг',
        }

        for category in Category.objects.all():
            if category.name_en in categories_translations:
                category.name_mk = categories_translations[category.name_en]
                category.save()
                self.stdout.write(f'Updated category: {category.name_en} -> {category.name_mk}')

        # Update Listings
        listings_translations = [
            {
                'title_en': 'Restaurant Destan',
                'title_mk': 'Ресторан Дестан',
                'address_en': 'Main Street 123, Gevgelija',
                'address_mk': 'Главна улица 123, Гевгелија',
                'open_time_en': 'Open until 23:00',
                'open_time_mk': 'Отворено до 23:00'
            },
            {
                'title_en': 'Hotel Apollonia',
                'title_mk': 'Хотел Аполонија', 
                'address_en': 'Central Square 5, Gevgelija',
                'address_mk': 'Централен плоштад 5, Гевгелија',
                'open_time_en': '24/7 Reception',
                'open_time_mk': '24/7 Рецепција'
            }
        ]

        for i, listing in enumerate(Listing.objects.all()):
            if i < len(listings_translations):
                data = listings_translations[i]
                for field, value in data.items():
                    setattr(listing, field, value)
                listing.save()
                self.stdout.write(f'Updated listing: {listing.title_en}')

        # Update Events
        events_translations = [
            {
                'title_en': 'Gevgelija Music Festival',
                'title_mk': 'Гевгелиски музички фестивал',
                'description_en': 'Annual music festival featuring local and international artists',
                'description_mk': 'Годишен музички фестивал со локални и меѓународни уметници',
                'location_en': 'City Park, Gevgelija',
                'location_mk': 'Градски парк, Гевгелија'
            }
        ]

        for i, event in enumerate(Event.objects.all()):
            if i < len(events_translations):
                data = events_translations[i]
                for field, value in data.items():
                    setattr(event, field, value)
                event.save()
                self.stdout.write(f'Updated event: {event.title_en}')

        self.stdout.write(self.style.SUCCESS('Successfully populated translations!'))