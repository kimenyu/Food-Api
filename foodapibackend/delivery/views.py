from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import Delivery, DeliveryStatusUpdate
from .serializers import DeliverySerializer, DeliveryCreateSerializer
from .utils import calculate_delivery_cost, get_distance, send_push_notification_to_user
from accounts.models import User
import environ
import os

# Initialize environment variables
env = environ.Env()


class DeliveryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing deliveries.
    """
    queryset = Delivery.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict deliveries based on the user's role:
        - Customers see their own deliveries.
        - Delivery agents see their assigned deliveries.
        - Owners see deliveries for their restaurant's orders.
        """
        user = self.request.user
        if user.role == 'customer':
            return self.queryset.filter(order__customer=user)
        elif user.role == 'delivery_agent':
            return self.queryset.filter(delivery_agent=user)
        elif user.role == 'owner':
            return self.queryset.filter(order__restaurant__user=user)
        return self.queryset.none()

    def get_serializer_class(self):
        """
        Use appropriate serializer based on the action.
        """
        if self.action == 'create':
            return DeliveryCreateSerializer
        return DeliverySerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new delivery.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delivery = serializer.save()
        response_serializer = DeliverySerializer(delivery)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Update the delivery status and log the change.
        """
        delivery = self.get_object()
        status_value = request.data.get('status')
        if status_value in dict(Delivery.STATUS_CHOICES):
            delivery.status = status_value
            if status_value == 'delivered':
                delivery.delivered_at = now()
            delivery.save()

            # Log status update
            DeliveryStatusUpdate.objects.create(
                delivery=delivery,
                status=status_value,
                updated_by=request.user
            )

            # Notify the customer about the status update
            if delivery.order.customer and delivery.order.customer.fcm_token:
                send_push_notification_to_user(
                    delivery.order.customer,
                    "Delivery Status Update",
                    f"Your delivery is now {status_value.replace('_', ' ').title()}!"
                )

            return Response({"message": f"Status updated to {status_value}"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='estimate-cost')
    def estimate_cost(self, request, pk=None):
        """
        Estimate the delivery cost based on the distance between pickup and dropoff locations.
        """
        delivery = self.get_object()
        distance, _ = get_distance(
            delivery.pickup_location,
            delivery.dropoff_location,
            api_key=env('GOOGLE_MAPS_API_KEY')
        )
        cost = calculate_delivery_cost(distance)
        return Response({"distance": distance, "cost": cost}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='update-location')
    def update_location(self, request, pk=None):
        """
        Update the real-time location of the delivery agent.
        """
        delivery = self.get_object()
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        if latitude and longitude:
            delivery.current_location = f"{latitude}, {longitude}"
            delivery.save()
            return Response({"message": "Location updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid location data"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='track')
    def track_order(self, request, pk=None):
        """
        Track the delivery's current status and location.
        """
        delivery = self.get_object()
        data = {
            "status": delivery.status,
            "current_location": delivery.current_location,
            "estimated_delivery_time": "15 minutes",  # Example placeholder for ETA
        }
        return Response(data, status=status.HTTP_200_OK)
