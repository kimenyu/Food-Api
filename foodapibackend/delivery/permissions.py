from rest_framework.permissions import IsAuthenticated


class IsDeliveryAgent(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.role == 'delivery_agent'
