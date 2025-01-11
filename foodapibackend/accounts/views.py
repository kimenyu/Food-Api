from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UpdateFCMTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        fcm_token = request.data.get('fcm_token')
        if not fcm_token:
            return Response({"error": "FCM token is required."}, status=400)

        user = request.user
        user.fcm_token = fcm_token
        user.save()
        return Response({"message": "FCM token updated successfully."})
