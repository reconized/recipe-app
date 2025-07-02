from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

class UserListCreateDestroyView(APIView):
    throttle_scope = 'users'
    throttle_classes = ScopedRateThrottle

class UploadView(APIView):
    throttle_scope = 'uploads'
    throttle_classes = ScopedRateThrottle