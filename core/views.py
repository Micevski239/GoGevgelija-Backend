from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Item, Listing, Event, Promotion, Blog
from .serializers import ItemSerializer, ListingSerializer, EventSerializer, PromotionSerializer, BlogSerializer, UserSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by("-created_at")
    serializer_class = ItemSerializer
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
