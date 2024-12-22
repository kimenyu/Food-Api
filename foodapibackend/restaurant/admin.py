from django.contrib import admin
from .models import Restaurant, MenuItem, Order, Notification, Review
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(Review)
