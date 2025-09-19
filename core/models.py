from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

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