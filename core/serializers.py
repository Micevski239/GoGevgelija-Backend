from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import Item, Category, Listing, Event, Promotion, Blog, EventJoin, Wishlist

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
            "category", "tags", "image", "phone_number", 
            "facebook_url", "instagram_url", "website_url", 
            "featured", "created_at", "updated_at"
        ]

class EventSerializer(serializers.ModelSerializer):
    has_joined = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            "id", "title", "description", "date_time", "location", 
            "cover_image", "entry_price", "category", "age_limit", "expectations", 
            "join_count", "has_joined", "featured", "created_at", "updated_at"
        ]
    
    def get_has_joined(self, obj):
        """Check if the current user has joined this event."""
        # TODO: Implement proper user join tracking when authentication is set up
        return False

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

class WishlistSerializer(serializers.ModelSerializer):
    item_type = serializers.CharField(read_only=True)
    item_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Wishlist
        fields = ["id", "item_type", "item_data", "created_at"]
        read_only_fields = ["user", "created_at"]
    
    def get_item_data(self, obj):
        """Serialize the actual content object based on its type."""
        content_object = obj.content_object
        if isinstance(content_object, Listing):
            return ListingSerializer(content_object).data
        elif isinstance(content_object, Event):
            return EventSerializer(content_object).data
        elif isinstance(content_object, Promotion):
            return PromotionSerializer(content_object).data
        return None

class WishlistCreateSerializer(serializers.Serializer):
    """Serializer for creating wishlist items."""
    item_type = serializers.ChoiceField(choices=['listing', 'event', 'promotion'])
    item_id = serializers.IntegerField()
    
    def create(self, validated_data):
        user = self.context['request'].user
        item_type = validated_data['item_type']
        item_id = validated_data['item_id']
        
        # Get the content type for the model
        model_mapping = {
            'listing': Listing,
            'event': Event,
            'promotion': Promotion,
        }
        
        model_class = model_mapping[item_type]
        content_type = ContentType.objects.get_for_model(model_class)
        
        # Check if the item exists
        try:
            content_object = model_class.objects.get(id=item_id)
        except model_class.DoesNotExist:
            raise serializers.ValidationError(f"{item_type.capitalize()} with id {item_id} does not exist.")
        
        # Create or get the wishlist item
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=item_id,
        )
        
        if not created:
            raise serializers.ValidationError("Item is already in wishlist.")
        
        return wishlist_item