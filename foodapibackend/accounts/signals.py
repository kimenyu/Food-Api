# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import User
# from restaurant.models import Restaurant, DeliveryAgent

# @receiver(post_save, sender=User)
# def create_role_specific_data(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'restaurant':
#             Restaurant.objects.create(user=instance)
#         elif instance.role == 'delivery_agent':
#             DeliveryAgent.objects.create(user=instance)
