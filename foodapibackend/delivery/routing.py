from django.urls import re_path
from .consumers import DeliveryTrackingConsumer

websocket_urlpatterns = [
    re_path(r'ws/delivery/(?P<order_id>\w+)/$', DeliveryTrackingConsumer.as_asgi()),
]
