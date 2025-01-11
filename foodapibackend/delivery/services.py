# from django.db.models import Q
# from django.contrib.gis.geos import Point
# from django.contrib.gis.db.models.functions import Distance
# import googlemaps
# from decimal import Decimal
# import logging
# from django.utils import timezone
# from .models import DeliveryAgentLocation, DeliveryTask

# logger = logging.getLogger(__name__)

# class DeliveryService:
#     def __init__(self):
#         self.gmaps = googlemaps.Client(key='YOUR_GOOGLE_MAPS_API_KEY')

#     def calculate_delivery_details(self, pickup_location, delivery_location):
#         """Calculate distance, duration and fee for delivery."""
#         try:
#             # Get route details from Google Maps
#             directions = self.gmaps.directions(
#                 pickup_location,
#                 delivery_location,
#                 mode="driving"
#             )

#             if not directions:
#                 raise ValueError("Could not calculate route")

#             route = directions[0]['legs'][0]
#             distance_km = route['distance']['value'] / 1000  # Convert meters to km
#             duration_mins = route['duration']['value'] / 60  # Convert seconds to minutes

#             # Calculate delivery fee
#             base_fee = Decimal('5.00')
#             fee_per_km = Decimal('2.00')
#             delivery_fee = base_fee + (Decimal(str(distance_km)) * fee_per_km)

#             return {
#                 'distance': round(distance_km, 2),
#                 'duration': round(duration_mins),
#                 'fee': round(delivery_fee, 2)
#             }
#         except Exception as e:
#             logger.error(f"Error calculating delivery details: {str(e)}")
#             raise

#     def find_available_agent(self, pickup_location, max_distance_km=5):
#         """Find the nearest available delivery agent."""
#         pickup_point = Point(
#             float(pickup_location['longitude']), 
#             float(pickup_location['latitude'])
#         )

#         # Query for available agents within radius
#         available_agents = DeliveryAgentLocation.objects.filter(
#             is_active=True,
#             agent__availability_status=True,
#             agent__user__is_active=True
#         ).annotate(
#             distance=Distance('longitude', 'latitude', pickup_point)
#         ).filter(
#             distance__lte=max_distance_km * 1000  # Convert km to meters
#         ).order_by('distance')

#         return available_agents.first().agent if available_agents.exists() else None

#     def create_delivery_task(self, order):
#         """Create a delivery task for an order."""
#         try:
#             # Get locations
#             pickup_location = {
#                 'latitude': order.restaurant.latitude,
#                 'longitude': order.restaurant.longitude,
#                 'address': order.restaurant.address
#             }
#             delivery_location = {
#                 'latitude': order.delivery_latitude,
#                 'longitude': order.delivery_longitude,
#                 'address': order.delivery_address
#             }

#             # Calculate delivery details
#             delivery_details = self.calculate_delivery_details(
#                 pickup_location['address'],
#                 delivery_location['address']
#             )

#             # Create delivery task
#             task = DeliveryTask.objects.create(
#                 order=order,
#                 pickup_location=pickup_location,
#                 delivery_location=delivery_location,
#                 estimated_distance=delivery_details['distance'],
#                 estimated_duration=delivery_details['duration'],
#                 delivery_fee=delivery_details['fee']
#             )

#             # Try to assign an agent
#             agent = self.find_available_agent(pickup_location)
#             if agent:
#                 self.assign_agent(task, agent)

#             return task

#         except Exception as e:
#             logger.error(f"Error creating delivery task: {str(e)}")
#             raise

#     def assign_agent(self, task, agent):
#         """Assign an agent to a delivery task."""
#         task.agent = agent
#         task.status = 'assigned'
#         task.assigned_at = timezone.now()
#         task.save()

#         # Send notification to agent
#         Notification.objects.create(
#             user=agent.user,
#             message=f"New delivery assignment for order #{task.order.id}",
#             order=task.order
#         )