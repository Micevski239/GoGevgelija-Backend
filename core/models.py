from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, help_text="Ionicon name (e.g., 'restaurant-outline')")
    trending = models.BooleanField(default=False, help_text="Show as trending category")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('cafe', 'Cafe'),
        ('bar', 'Bar'),
        ('hotel', 'Hotel'),
        ('shop', 'Shop'),
        ('service', 'Service'),
        ('attraction', 'Attraction'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    address = models.CharField(max_length=500)
    open_time = models.CharField(max_length=100, help_text="e.g., 'Open until 23:00' or 'Mon-Fri 9:00-18:00'")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    tags = models.JSONField(default=list, help_text="List of tags, e.g., ['Grill', 'Family', 'Outdoor']")
    image = models.URLField(max_length=1000, help_text="URL to the listing image")
    featured = models.BooleanField(default=False, help_text="Show in featured section")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text="Event description")
    date_time = models.CharField(max_length=100, help_text="e.g., 'Fri, 20:00' or 'Dec 25, 18:00'")
    location = models.CharField(max_length=255, help_text="Event venue/location")
    cover_image = models.URLField(max_length=1000, help_text="URL to the event cover image")
    featured = models.BooleanField(default=False, help_text="Show in featured events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.date_time}"


class Promotion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text="Promotion description")
    discount_code = models.CharField(max_length=50, help_text="Promo code for discount")
    tags = models.JSONField(default=list, help_text="List of tags, e.g., ['Today', 'Dine-in', '50% off']")
    image = models.URLField(max_length=1000, help_text="URL to the promotion image")
    valid_until = models.DateField(null=True, blank=True, help_text="Promotion expiry date")
    featured = models.BooleanField(default=False, help_text="Show in featured promotions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.discount_code}"


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('guide', 'Travel Guide'),
        ('food', 'Food & Dining'),
        ('culture', 'Culture & History'),
        ('events', 'Events & Activities'),
        ('tips', 'Travel Tips'),
        ('news', 'Local News'),
        ('lifestyle', 'Lifestyle'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True, help_text="Brief subtitle or summary")
    content = models.TextField(help_text="Full blog post content")
    author = models.CharField(max_length=100, default="GoGevgelija Team")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    tags = models.JSONField(default=list, help_text="List of tags, e.g., ['Travel', 'Food', 'Culture']")
    cover_image = models.URLField(max_length=1000, help_text="URL to the blog cover image")
    read_time_minutes = models.PositiveIntegerField(default=5, help_text="Estimated reading time in minutes")
    featured = models.BooleanField(default=False, help_text="Show in featured blogs")
    published = models.BooleanField(default=True, help_text="Whether the blog is published")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
class test(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title