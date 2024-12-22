from .views import RestaurantCreateAPIView, RestaurantListAPIView, RestaurantRetrieveAPIView, RestaurantUpdateAPIView, RestaurantDeleteAPIView
from django.urls import path

urlpatterns = [
    path('create/', RestaurantCreateAPIView.as_view(), name='restaurant-create'),
    path('list/', RestaurantListAPIView.as_view(), name='restaurant-list'),
    path('retrieve/<int:pk>/', RestaurantRetrieveAPIView.as_view(), name='restaurant-retrieve'),
    path('update/<int:pk>/', RestaurantUpdateAPIView.as_view(), name='restaurant-update'),
    path('delete/<int:pk>/', RestaurantDeleteAPIView.as_view(), name='restaurant-delete'),
]

