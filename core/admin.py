from django.contrib import admin
from .models import Item, Listing, Event, Promotion

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'rating', 'featured', 'created_at')
    list_filter = ('category', 'featured', 'created_at')
    search_fields = ('title', 'address', 'category')
    list_editable = ('featured',)
    ordering = ('-created_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'location', 'featured', 'created_at')
    list_filter = ('featured', 'created_at')
    search_fields = ('title', 'location', 'description')
    list_editable = ('featured',)
    ordering = ('-created_at',)

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_code', 'valid_until', 'featured', 'created_at')
    list_filter = ('featured', 'valid_until', 'created_at')
    search_fields = ('title', 'discount_code', 'description')
    list_editable = ('featured',)
    ordering = ('-created_at',)
