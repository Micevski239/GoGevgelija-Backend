from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ItemViewSet, ListingViewSet, health, Register, Me
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"items", ItemViewSet, basename="item")
router.register(r"listings", ListingViewSet, basename="listing")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("api/health/", health),
    path("api/auth/register/", Register.as_view()),
    path("api/auth/me/", Me.as_view()),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
