from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from apps.recipe_api.models.category import Category
from apps.recipe_api.serializers import CategorySerializer

def locked_out_view(request):
    return render(request, 'locked_out.html')

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer