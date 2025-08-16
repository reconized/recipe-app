from rest_framework import viewsets
from django.db import transaction
from apps.recipes.models.cuisine import Cuisine
from apps.recipes.models.category import Category
from apps.recipes.serializers.cuisine import CuisineSerializer
from apps.recipes.serializers.category import CategorySerializer
from apps.recipes.permissions import IsStaffOrManager

class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all().select_related("parent").prefetch_related("subcategories").order_by("name")
    serializer_class = CuisineSerializer
    permission_classes = [IsStaffOrManager]

    def get_queryset(self):
        qs = super().get_queryset()
        parent_id = self.request.query_params.get("parent")
        if parent_id is not None:
            qs = qs.filter(parent_id=parent_id)
        return qs
    
    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()
    
    @transaction.atomic
    def perform_destroy(self, instance):
        instance.save()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrManager]

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()

    @transaction.atomic
    def perform_destroy(self, instance):
        instance.save()