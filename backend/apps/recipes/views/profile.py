from rest_framework import viewsets
from django.db import transaction
from django.contrib.auth.models import User
from apps.recipes.models.user_profile import Profile
from apps.recipes.serializers.profile import ProfileSerializer
from apps.recipes.permissions_profile import IsSelfOrAdmin

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [IsSelfOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(user_id=self.request.user.id)
    
    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()
        