from django.db import transaction
from django.db.models import Count, Q, Prefetch
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.recipes.models.recipe import Recipe
from apps.recipes.models.instruction import Instruction
from apps.recipes.serializers.recipe import RecipeSerializer, RecipeDetailSerializer
from apps.recipes.permissions import IsOwnerOrReadOnly
from apps.recipes.filters.recipe_filter import RecipeFilter

class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = RecipeFilter
    search_fields = ["title", "description", "category__name", "cuisines__name"]
    ordering_fields = ["title", "created_at", "prep_time", "cook_time"]
    ordering = ["-created_at"]

    def _base_queryset(self):
        return (
            Recipe.objects
            .select_related("category", "user")
            .prefetch_related("cuisines")
            .distinct()
        )
    
    def get_queryset(self):
        qs = self._base_queryset()

        # Ingredients + Instructions only for retrieve
        if getattr(self, "action", None) == "retrieve":
            qs = qs.prefetch_related(
                "ingredients",
                Prefetch("instructions", queryset=Instruction.objects.order_by("step_number")),
            )
        
        # Nested filters from router params
        cuisine_id = self.kwargs.get("cuisine_pk")
        category_id = self.kwargs.get("category_pk")
        if cuisine_id:
            qs = qs.filter(cuisines__id=cuisine_id)
        if category_id:
            qs = qs.filter(category__id=category_id)

        return qs
    
    # Serializers
    def get_serializer_class(self):
        return RecipeDetailSerializer if self.action == "retrieve" else RecipeSerializer
    
    # Writes atomic
    def perform_create(self, serializer):
        """
        - Attach owner automatically
        - If nested under /categories/{id}/recipes/, set category
        - If nested under /cuisines/{id}/recipes/, add that cuisine to M2M
        - Serializer has to be validated with the category and cuisine
        """
        category_pk = self.kwargs.get("category_pk")
        cuisine_pk = self.kwargs.get("cuisine_pk")  

        recipe = serializer.save(
            user=self.request.user,
            **({"category_id": category_pk} if category_pk else {})
        )
        if cuisine_pk:
            recipe.cuisines.add(int(cuisine_pk))

    @transaction.atomic
    def perform_update(self, serializer):
        """
        - If nested under /categories/{id}/recipes/, force category
        - If nested under /cuisines/{id}/recipes/, ensure cuisine is attached
        """
        category_pk = self.kwargs.get("category_pk")
        cuisine_pk = self.kwargs.get("cuisine_pk")

        recipe = serializer.save()

        if category_pk and recipe.category_id != int(category_pk):
            recipe.category_id = int(category_pk)
            recipe.save(update_fields=["category"])

        if cuisine_pk:
            recipe.cuisines.add(int(cuisine_pk))

    @transaction.atomic
    def perform_destroy(self, instance):
        instance.delete()

    # Personalized feed
    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def feed(self, request):
        """
        - If authenticated: boost recipe in cuisines the user has used before
        - Else recent recipes
        Supports: ?limit=20 and optional ?cuisines=1,2,3 to force cuisines filters
        """
        limit = int(request.query_params.get("limit", 20))
        force_cuisines = request.query_params.getlist("cuisines")

        qs = (
            Recipe.objects
            .select_related("category", "user")
            .prefetch_related("cuisines")
            .order_by("-created_at")
            .distinct()
        )

        # Allow client to force cuisines filter: /recipes/feed?cuisines=1,2
        if force_cuisines:
            ids = [int(x) for x in force_cuisines.split(",") if x.strip().isdigit()]
            if ids:
                qs = qs.filter(cuisines__id__in=ids).distinct()
                data = self.get_serializer(qs[:limit], many=True).data
                return Response(data)
            
        # Personalization
        if request.user.is_authenticated:
            # Find cuisines the user has cooked with (by frequency)
            user_cuisine_counts = (
                Recipe.objects.filter(user=request.user)
                .values("cuisines__id")
                .exclude(cuisines__id=None)
                .annotate(n=Count(id))
                .order_by("-n")
            )
            user_pref_ids = [row["cuisines__id"] for row in user_cuisine_counts if row["cuisines__id"]]

            if user_pref_ids:
                preferred = qs.filter(cuisines__id__in=user_pref_ids)[:limit]
                remaining = limit - preferred.count()
                if remaining > 0:
                    others = qs.exclude(id__in=preferred.values("id"))[:remaining]
                    out = list(preferred) + list(others)
                else:
                    out = list(preferred)
                data = self.get_serializer(out, many=True).data
                return Response(data)

        # Anonymous or no preferences: just recent recipes
        data = self.get_serializer(qs[:limit], many=True).data
        return Response(data)
