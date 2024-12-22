from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .serializers import RestaurantSerializer, MenuItemSerializer, OrderSerializer, NotificationSerializer, ReviewSerializer
from .models import Restaurant, MenuItem, Order, Notification, Review
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRestaurantUser


class RestaurantCreateAPIView(CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantUser]

    def perform_create(self, serializer):
        # Ensure the user is automatically linked to the restaurant
        serializer.save(user=self.request.user)
    
class RestaurantListAPIView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
class RestaurantRetrieveAPIView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    def get_queryset(self):
        # Restrict restaurants to updating only their data
        return Restaurant.objects.filter(user=self.request.user)
    
class RestaurantUpdateAPIView(UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    def get_queryset(self):
        # Restrict restaurants to updating only their data
        return Restaurant.objects.filter(user=self.request.user)
    
class RestaurantDeleteAPIView(DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    def get_queryset(self):
        # Restrict restaurants to updating only their data
        return Restaurant.objects.filter(user=self.request.user)
