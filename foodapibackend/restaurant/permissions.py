from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


# Custom Permissions
class IsOwner(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.role == 'owner'

class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Check if the menu item's restaurant's user matches the request user
        return obj.restaurant.user == request.user and request.user.role == 'owner'

class IsCustomer(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.role == 'customer'

class IsDeliveryAgent(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.role == 'delivery_agent'
