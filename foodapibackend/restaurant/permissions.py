from rest_framework.permissions import BasePermission

class IsRestaurantUser(BasePermission):
    """
    Allow access only to users with the role 'restaurant'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'restaurant'
