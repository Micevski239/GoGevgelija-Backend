from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item, Category, Listing, Event, Promotion, Blog

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id","name","created_at"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "icon", "trending", "created_at"]

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "id", "title", "rating", "address", "open_time", 
            "category", "tags", "image", "featured", 
            "created_at", "updated_at"
        ]

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id", "title", "description", "date_time", "location", 
            "cover_image", "featured", "created_at", "updated_at"
        ]

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            "id", "title", "description", "discount_code", "tags", 
            "image", "valid_until", "featured", "created_at", "updated_at"
        ]

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id", "title", "subtitle", "content", "author", "category", 
            "tags", "cover_image", "read_time_minutes", "featured", 
            "published", "created_at", "updated_at"
        ]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ["username", "email", "password"]
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email",""),
            password=validated_data["password"],
        )