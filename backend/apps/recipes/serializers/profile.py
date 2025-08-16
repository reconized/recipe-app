from rest_framework import serializers
from apps.recipes.models.user_profile import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'display_name']
        read_only_fields = ['user', 'username']