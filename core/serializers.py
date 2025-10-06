from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import translation
from .models import Item, Category, Listing, Event, Promotion, Blog, EventJoin, Wishlist, UserProfile

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id","name","created_at"]

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ["id", "name", "icon", "trending", "created_at"]
    
    def get_name(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'name_{language}', obj.name_en or obj.name)

class ListingSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    open_time = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    working_hours = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "address", "open_time", 
            "category", "tags", "working_hours", "image", "phone_number", 
            "facebook_url", "instagram_url", "website_url", 
            "featured", "created_at", "updated_at"
        ]
    
    def get_title(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'title_{language}', obj.title_en or obj.title)
    
    def get_description(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'description_{language}', obj.description_en or obj.description)
    
    def get_address(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'address_{language}', obj.address_en or obj.address)
    
    def get_open_time(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'open_time_{language}', obj.open_time_en or obj.open_time)
    
    def get_tags(self, obj):
        language = self.context.get('language', 'en')
        if language == 'mk' and obj.tags_mk:
            return obj.tags_mk
        return obj.tags
    
    def get_working_hours(self, obj):
        language = self.context.get('language', 'en')
        if language == 'mk' and obj.working_hours_mk:
            return obj.working_hours_mk
        return obj.working_hours

class EventSerializer(serializers.ModelSerializer):
    has_joined = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    entry_price = serializers.SerializerMethodField()
    age_limit = serializers.SerializerMethodField()
    expectations = serializers.SerializerMethodField()
    
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
    
    def get_title(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'title_{language}', obj.title_en or obj.title)
    
    def get_description(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'description_{language}', obj.description_en or obj.description)
    
    def get_location(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'location_{language}', obj.location_en or obj.location)
    
    def get_entry_price(self, obj):
        language = self.context.get('language', 'en')
        if language == 'mk' and obj.entry_price_mk:
            return obj.entry_price_mk
        return obj.entry_price
    
    def get_age_limit(self, obj):
        language = self.context.get('language', 'en')
        if language == 'mk' and obj.age_limit_mk:
            return obj.age_limit_mk
        return obj.age_limit
    
    def get_expectations(self, obj):
        language = self.context.get('language', 'en')
        if language == 'mk' and obj.expectations_mk:
            return obj.expectations_mk
        return obj.expectations

class PromotionSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = Promotion
        fields = [
            "id", "title", "description", "has_discount_code", "discount_code", "tags", 
            "image", "valid_until", "featured", "website", "facebook_url", 
            "instagram_url", "address", "created_at", "updated_at"
        ]
    
    def get_title(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'title_{language}', obj.title_en or obj.title)
    
    def get_description(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'description_{language}', obj.description_en or obj.description)
    
    def get_address(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'address_{language}', obj.address_en or obj.address)
    
    def get_tags(self, obj):
        language = self.context.get('language', 'en')
        if language == 'mk' and obj.tags_mk:
            return obj.tags_mk
        return obj.tags

class BlogSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subtitle = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = [
            "id", "title", "subtitle", "content", "author", "category", 
            "tags", "cover_image", "read_time_minutes", "featured", 
            "published", "created_at", "updated_at"
        ]
    
    def get_title(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'title_{language}', obj.title_en or obj.title)
    
    def get_subtitle(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'subtitle_{language}', obj.subtitle_en or obj.subtitle)
    
    def get_content(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'content_{language}', obj.content_en or obj.content)
    
    def get_author(self, obj):
        language = self.context.get('language', 'en')
        return getattr(obj, f'author_{language}', obj.author_en or obj.author)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["language_preference"]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile"]
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email",""),
            password=validated_data["password"],
        )
        # Create user profile with default language
        UserProfile.objects.create(user=user)
        return user

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
        elif isinstance(content_object, Blog):
            return BlogSerializer(content_object).data
        return None

class WishlistCreateSerializer(serializers.Serializer):
    """Serializer for creating wishlist items."""
    item_type = serializers.ChoiceField(choices=['listing', 'event', 'promotion', 'blog'])
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
            'blog': Blog,
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