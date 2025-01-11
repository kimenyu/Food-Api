from rest_framework import serializers
from .models import Delivery, DeliveryStatusUpdate
from restaurant.models import Order
from accounts.models import User


class DeliveryStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery Status Updates
    """

    updated_by = serializers.StringRelatedField()  # Display the username or email of the user who updated the status

    class Meta:
        model = DeliveryStatusUpdate
        fields = ['id', 'status', 'updated_at', 'updated_by']


class DeliverySerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery
    """
    order_details = serializers.SerializerMethodField()
    delivery_agent_name = serializers.StringRelatedField(source='delivery_agent', read_only=True)
    status_updates = DeliveryStatusUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'id',
            'order',  # Foreign key to Order
            'order_details',  # Nested order details
            'delivery_agent',  # Foreign key to User (delivery agent)
            'delivery_agent_name',
            'delivery_address',
            'pickup_location',
            'dropoff_location',
            'current_location',
            'cost',
            'status',
            'delivered_at',
            'created_at',
            'updated_at',
            'status_updates',  # History of status updates
        ]
        read_only_fields = ['status_updates', 'created_at', 'updated_at']

    def get_order_details(self, obj):
        """
        Return minimal details about the order.
        """
        return {
            'order_id': obj.order.id,
            'customer_name': obj.order.customer.email,
            'restaurant_name': obj.order.restaurant.name,
            'total_price': obj.order.total_price,
        }


class DeliveryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating deliveries
    """
    class Meta:
        model = Delivery
        fields = ['order', 'delivery_address', 'pickup_location', 'dropoff_location']

    def validate(self, data):
        """
        Validate that the order has not already been assigned a delivery.
        """
        order = data.get('order')
        if Delivery.objects.filter(order=order).exists():
            raise serializers.ValidationError("A delivery has already been created for this order.")
        return data
