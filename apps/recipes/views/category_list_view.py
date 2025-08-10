from rest_framework import generics
from rest_framework import permissions
from apps.recipes.models.category import Category
from apps.recipes.serializers.category_serializer import CategorySerializer

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]