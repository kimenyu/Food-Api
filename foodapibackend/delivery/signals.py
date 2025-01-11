from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Delivery
from accounts.models import User
from .utils import find_nearest_driver
from .tasks import push_notification

@receiver(post_save, sender=Delivery)
def notify_on_status_change(sender, instance, **kwargs):
    if instance.status == 'accepted':
        push_notification.delay(instance.customer.fcm_token, "Order Accepted", "Your order has been accepted!")
    elif instance.status == 'in_transit':
        push_notification.delay(instance.customer.fcm_token, "On the Way", "Your order is on the way!")
    elif instance.status == 'delivered':
        push_notification.delay(instance.customer.fcm_token, "Delivered", "Your order has been delivered!")
        

@receiver(post_save, sender=Delivery)
def assign_driver(sender, instance, created, **kwargs):
    if created and not instance.delivery_agent:
        drivers = User.objects.filter(role='delivery_agent', is_active=True)
        order_location = (instance.dropoff_latitude, instance.dropoff_longitude)
        nearest_driver = find_nearest_driver(order_location, drivers)
        if nearest_driver:
            instance.delivery_agent = nearest_driver
            instance.save()

