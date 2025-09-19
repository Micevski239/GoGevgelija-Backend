from django.contrib import admin
from .models import Item, Listing

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
