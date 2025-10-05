from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Item, Category, Listing, Event, Promotion, Blog, EventJoin, Wishlist
from .serializers import ItemSerializer, CategorySerializer, ListingSerializer, EventSerializer, PromotionSerializer, BlogSerializer, UserSerializer, WishlistSerializer, WishlistCreateSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by("-created_at")
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get only featured listings"""
        featured_listings = Listing.objects.filter(featured=True)
        serializer = self.get_serializer(featured_listings, many=True)
        return Response(serializer.data)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get only featured events"""
        featured_events = Event.objects.filter(featured=True)
        serializer = self.get_serializer(featured_events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def join(self, request, pk=None):
        """Join an event with proper user tracking"""
        event = self.get_object()
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user already joined
            existing_join = EventJoin.objects.filter(event=event, user=request.user).first()
            if existing_join:
                return Response({
                    'error': 'You have already joined this event'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create join record
            EventJoin.objects.create(event=event, user=request.user)
            
            # Update join count
            event.join_count = EventJoin.objects.filter(event=event).count()
            event.save()
        else:
            # For non-authenticated users, just increment count
            event.join_count += 1
            event.save()
        
        serializer = self.get_serializer(event)
        return Response({
            'message': 'Successfully joined the event!',
            'event': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def unjoin(self, request, pk=None):
        """Unjoin an event (leave the event)"""
        event = self.get_object()
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user has joined
            existing_join = EventJoin.objects.filter(event=event, user=request.user).first()
            if not existing_join:
                return Response({
                    'error': 'You have not joined this event'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Remove join record
            existing_join.delete()
            
            # Update join count
            event.join_count = EventJoin.objects.filter(event=event).count()
            event.save()
        else:
            # For non-authenticated users, just decrement count (but not below 0)
            if event.join_count > 0:
                event.join_count -= 1
                event.save()
        
        serializer = self.get_serializer(event)
        return Response({
            'message': 'Successfully left the event!',
            'event': serializer.data
        }, status=status.HTTP_200_OK)

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get only featured promotions"""
        featured_promotions = Promotion.objects.filter(featured=True)
        serializer = self.get_serializer(featured_promotions, many=True)
        return Response(serializer.data)

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(published=True)
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get only featured blogs"""
        featured_blogs = Blog.objects.filter(featured=True, published=True)
        serializer = self.get_serializer(featured_blogs, many=True)
        return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(_request):
    return Response({"status": "ok"})

class Register(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        s = UserSerializer(data = request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {"id": user.id, "username": user.username, "email": user.email},
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status = status.HTTP_201_CREATED)

class Me(APIView):
    def get(self, request):
        u = request.user
        return Response({"id": u.id, "username": u.username, "email": u.email})
    
    def put(self, request):
        """Update user profile"""
        user = request.user
        data = request.data
        
        # Update username if provided
        if 'username' in data and data['username']:
            # Check if username already exists
            if User.objects.filter(username=data['username']).exclude(id=user.id).exists():
                return Response(
                    {"error": "Username already exists"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.username = data['username']
        
        # Handle password change if provided
        if 'new_password' in data and data['new_password']:
            # Verify current password if provided
            if 'current_password' in data and data['current_password']:
                if not user.check_password(data['current_password']):
                    return Response(
                        {"error": "Current password is incorrect"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Set new password
            user.set_password(data['new_password'])
        
        # Save user changes
        user.save()
        
        return Response({
            "id": user.id, 
            "username": user.username, 
            "email": user.email
        })

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return wishlist items for the current user only."""
        return Wishlist.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Add an item to the user's wishlist."""
        serializer = WishlistCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        wishlist_item = serializer.save()
        
        # Return the created wishlist item using the main serializer
        response_serializer = WishlistSerializer(wishlist_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def remove(self, request):
        """Remove an item from wishlist by item_type and item_id."""
        item_type = request.data.get('item_type')
        item_id = request.data.get('item_id')
        
        if not item_type or not item_id:
            return Response(
                {"error": "Both item_type and item_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the content type for the model
        model_mapping = {
            'listing': Listing,
            'event': Event,
            'promotion': Promotion,
            'blog': Blog,
        }
        
        if item_type not in model_mapping:
            return Response(
                {"error": "Invalid item_type. Must be 'listing', 'event', 'promotion', or 'blog'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        model_class = model_mapping[item_type]
        content_type = ContentType.objects.get_for_model(model_class)
        
        try:
            wishlist_item = Wishlist.objects.get(
                user=request.user,
                content_type=content_type,
                object_id=item_id
            )
            wishlist_item.delete()
            return Response({"message": "Item removed from wishlist."}, status=status.HTTP_200_OK)
        except Wishlist.DoesNotExist:
            return Response(
                {"error": "Item not found in wishlist."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def check(self, request):
        """Check if an item is in the user's wishlist."""
        item_type = request.data.get('item_type')
        item_id = request.data.get('item_id')
        
        if not item_type or not item_id:
            return Response(
                {"error": "Both item_type and item_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the content type for the model
        model_mapping = {
            'listing': Listing,
            'event': Event,
            'promotion': Promotion,
            'blog': Blog,
        }
        
        if item_type not in model_mapping:
            return Response(
                {"error": "Invalid item_type. Must be 'listing', 'event', 'promotion', or 'blog'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        model_class = model_mapping[item_type]
        content_type = ContentType.objects.get_for_model(model_class)
        
        is_wishlisted = Wishlist.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=item_id
        ).exists()
        
        return Response({"is_wishlisted": is_wishlisted}, status=status.HTTP_200_OK)
