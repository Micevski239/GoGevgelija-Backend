from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item, Listing

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id","name","created_at"]

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "id", "title", "rating", "address", "open_time", 
            "category", "tags", "image", "featured", 
            "created_at", "updated_at"
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