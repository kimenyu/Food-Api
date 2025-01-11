from django.contrib import admin
from .models import DeliveryAgent, DeliveryAgentLocation, DeliveryTask
# Register your models here.

admin.site.register(DeliveryAgent)
admin.site.register(DeliveryAgentLocation)
admin.site.register(DeliveryTask)
