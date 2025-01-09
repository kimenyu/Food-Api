from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, 
    UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwner, IsOwnerOrReadOnly, IsCustomer

from .models import Restaurant, MenuItem, Order, Review, DeliveryAgent
from .serializers import (
    RestaurantSerializer, RestaurantCreateSerializer, RestaurantUpdateSerializer,
    MenuItemSerializer, MenuItemCreateSerializer,
    OrderSerializer, OrderCreateSerializer,
    ReviewSerializer, ReviewCreateSerializer
)


# Restaurant Views
class RestaurantCreateView(CreateAPIView):
    serializer_class = RestaurantCreateSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'owner'):
            raise PermissionDenied("You already have a restaurant registered")
        serializer.save(user=self.request.user)

class RestaurantListView(ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

class RestaurantDetailView(RetrieveAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

class RestaurantUpdateView(UpdateAPIView):
    serializer_class = RestaurantUpdateSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        restaurant = self.get_object()
        if restaurant.user != self.request.user:
            raise PermissionDenied("You don't have permission to update this restaurant")
        serializer.save()

class RestaurantDeleteView(DestroyAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You don't have permission to delete this restaurant")
        instance.delete()

# MenuItem Views
class MenuItemCreateView(CreateAPIView):
    serializer_class = MenuItemCreateSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(user=self.request.user)
        serializer.save(restaurant=restaurant)

class MenuItemListView(ListAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return MenuItem.objects.filter(restaurant_id=self.kwargs['restaurant_id'])

class MenuItemUpdateView(UpdateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]  # Just check if user is authenticated
    queryset = MenuItem.objects.all()

    def perform_update(self, serializer):
        menu_item = self.get_object()
        if menu_item.restaurant.user != self.request.user or self.request.user.role != 'owner':
            raise PermissionDenied("You don't have permission to update this menu item")
        serializer.save()

class MenuItemDeleteView(DestroyAPIView):
    queryset = MenuItem.objects.all()
    permission_classes = [IsAuthenticated]  # Just check if user is authenticated

    def perform_destroy(self, instance):
        if instance.restaurant.user != self.request.user or self.request.user.role != 'owner':
            raise PermissionDenied("You don't have permission to delete this menu item")
        instance.delete()

# Order Views
class OrderCreateView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        # Use the default create implementation to save the order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(customer=self.request.user)

        # Use OrderSerializer for the response
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(customer=user)
        elif user.role == 'owner':
            return Order.objects.filter(restaurant__user=user)
        elif user.role == 'delivery_agent':
            return Order.objects.filter(delivery_agent=user)
        return Order.objects.none()

class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(customer=user)
        elif user.role == 'owner':
            return Order.objects.filter(restaurant__user=user)
        elif user.role == 'delivery_agent':
            return Order.objects.filter(delivery_agent=user)
        return Order.objects.none()

# Review Views
class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsCustomer]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['restaurant_id'] = self.kwargs.get('restaurant_id')
        return context

class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(restaurant_id=self.kwargs['restaurant_id'])

class RestaurantReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'owner':
            return Review.objects.filter(restaurant__user=user)
        return Review.objects.none()

