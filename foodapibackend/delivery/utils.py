import firebase_admin
from firebase_admin import messaging, credentials
from foodapibackend import settings
import firebase_admin
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from geopy.distance import geodesic


cred = credentials.Certificate(settings.FIREBASE_CONFIG)
firebase_admin.initialize_app(cred)

def send_push_notification(registration_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=registration_token,
    )
    response = messaging.send(message)
    return response



def find_nearest_driver(order_location, drivers):
    nearest_driver = None
    min_distance = float('inf')
    for driver in drivers:
        driver_location = (driver.latitude, driver.longitude)
        distance = geodesic(order_location, driver_location).km
        if distance < min_distance:
            min_distance = distance
            nearest_driver = driver
    return nearest_driver


def calculate_delivery_cost(distance, base_rate=50, rate_per_km=10):
    return base_rate + (distance * rate_per_km)



def broadcast_delivery_update(order_id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"delivery_{order_id}",
        {
            "type": "send_delivery_update",
            "data": data
        }
    )
