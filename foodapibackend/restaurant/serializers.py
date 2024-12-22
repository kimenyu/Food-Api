from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem, Notification, Review

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    menu_items = MenuItemSerializer(many=True, read_only=True)  # Display MenuItem details

    class Meta:
        model = Restaurant
        fields = ['id', 'user', 'name', 'description', 'address', 'contact_number', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        # Automatically assign the current authenticated user as the restaurant owner
        user = self.context['request'].user
        return Restaurant.objects.create(user=user, **validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)  # Display MenuItem details
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menu_item', write_only=True
    )  # Allow passing menu_item ID during creation

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderItemSerializer(many=True, read_only=True)  # Nested OrderItem details
    order_items_data = OrderItemSerializer(many=True, write_only=True)  # For creating OrderItems

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'restaurant',
            'delivery_agent',
            'status',
            'total_price',
            'order_items',
            'order_items_data',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items_data')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Notification
        fields = ['id', 'user', 'order', 'message', 'is_read', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    class Meta:
        model = Review
        fields = ['id', 'customer', 'restaurant', 'rating', 'comment', 'created_at']
