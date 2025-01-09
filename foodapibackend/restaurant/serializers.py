from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem, Review, DeliveryAgent, Notification

class MenuItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'is_available']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def create(self, validated_data):
        restaurant_id = self.context['restaurant_id']
        user = self.context['request'].user
        return Review.objects.create(
            customer=user,
            restaurant_id=restaurant_id,
            **validated_data
        )

class ReviewSerializer(serializers.ModelSerializer):
    customer_email = serializers.EmailField(source='customer.email', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'customer_email', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

    def validate_menu_item(self, value):
        if not value.is_available:
            raise serializers.ValidationError("This menu item is currently unavailable")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'price']
        read_only_fields = ['price']

class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['restaurant', 'order_items']

    def validate_restaurant(self, value):
        # Add any restaurant-specific validation (e.g., checking if restaurant is active)
        return value

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        user = self.context['request'].user
        
        # Calculate total price
        total_price = sum(
            item['menu_item'].price * item['quantity']
            for item in order_items_data
        )
        
        # Create order
        order = Order.objects.create(
            customer=user,
            total_price=total_price,
            **validated_data
        )
        
        # Create order items
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                price=item_data['menu_item'].price,
                **item_data
            )
        
        return order

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    customer_email = serializers.EmailField(source='customer.email', read_only=True)
    delivery_agent_email = serializers.EmailField(source='delivery_agent.email', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_email', 'restaurant_name', 'delivery_agent_email',
                 'status', 'total_price', 'created_at', 'updated_at', 'order_items']
        read_only_fields = ['total_price', 'created_at', 'updated_at']

class RestaurantCreateSerializer(serializers.ModelSerializer):
    menu_items = MenuItemCreateSerializer(many=True, required=False)

    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'address', 'contact_number', 'menu_items']

    def create(self, validated_data):
        menu_items_data = validated_data.pop('menu_items', [])
        
        # Create restaurant (user is passed automatically via serializer.save)
        restaurant = Restaurant.objects.create(**validated_data)
        
        # Create menu items
        for item_data in menu_items_data:
            MenuItem.objects.create(restaurant=restaurant, **item_data)
        
        return restaurant

class RestaurantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'address', 'contact_number']

    def validate_contact_number(self, value):
        if not value.replace('+', '').replace('-', '').isdigit():
            raise serializers.ValidationError("Contact number must contain only digits, '+', and '-'")
        return value

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    owner_email = serializers.EmailField(source='user.email', read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'address', 'contact_number',
                 'rating', 'created_at', 'owner_email', 'menu_items',
                 'reviews', 'average_rating']
        read_only_fields = ['rating', 'created_at']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0.0
        return sum(review.rating for review in reviews) / len(reviews)