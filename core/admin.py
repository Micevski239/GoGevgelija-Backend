from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Item, Category, Listing, Event, Promotion, Blog, test, EventJoin, Wishlist

@admin.register(test)
class testAdmib(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'icon', 'trending', 'created_at')
    list_filter = ('trending', 'created_at')
    search_fields = ('name', 'icon')
    list_editable = ('trending',)
    ordering = ('name',)

@admin.register(Listing)
class ListingAdmin(TranslationAdmin):
    list_display = ('title', 'category', 'rating', 'featured', 'created_at', 'phone_number', 'facebook_url', 'instagram_url', 'website_url')
    list_filter = ('category', 'featured', 'created_at')
    search_fields = ('title', 'address', 'category')
    list_editable = ('featured',)
    ordering = ('-created_at',)

@admin.register(Event)
class EventAdmin(TranslationAdmin):
    list_display = ('title', 'date_time', 'location', 'category', 'featured', 'created_at')
    list_filter = ('category', 'featured', 'created_at')
    search_fields = ('title', 'location', 'description', 'category')
    list_editable = ('featured',)
    ordering = ('-created_at',)

@admin.register(Promotion)
class PromotionAdmin(TranslationAdmin):
    list_display = ('title', 'discount_code', 'valid_until', 'featured', 'created_at')
    list_filter = ('featured', 'valid_until', 'created_at')
    search_fields = ('title', 'discount_code', 'description')
    list_editable = ('featured',)
    ordering = ('-created_at',)

@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ('title', 'author', 'category', 'read_time_minutes', 'featured', 'published', 'created_at')
    list_filter = ('category', 'featured', 'published', 'created_at')
    search_fields = ('title', 'subtitle', 'content', 'author', 'category')
    list_editable = ('featured', 'published')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(EventJoin)
class EventJoinAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'created_at')
    list_filter = ('created_at', 'event')
    search_fields = ('user__username', 'user__email', 'event__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'content_object', 'item_type', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
