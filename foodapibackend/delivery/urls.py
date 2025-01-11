from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeliveryViewSet

# Create a router for the DeliveryViewSet
router = DefaultRouter()
router.register(r'deliveries', DeliveryViewSet, basename='delivery')

urlpatterns = [
    path('', include(router.urls)),  # Include all router-generated URLs
]
