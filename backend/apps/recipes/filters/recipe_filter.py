import django_filters
from django.db.models import Q
from apps.recipes.models.recipe import Recipe

class RecipeFilter(django_filters.FilterSet):
    cuisine = django_filters.CharFilter(method="filter_cuisines")
    cuisines = django_filters.CharFilter(method="filter_cuisines")
    category = django_filters.NumberFilter(field_name="category__name", lookup_expr="icontains")
    category_id = django_filters.NumberFilter(field_name="category_id")
    min_prep_time = django_filters.NumberFilter(field_name="prep_time", lookup_expr="gte")
    max_prep_time = django_filters.NumberFilter(field_name="prep_time", lookup_expr="lte")
    min_cook_time = django_filters.NumberFilter(field_name="cook_time", lookup_expr="gte")
    max_cook_time = django_filters.NumberFilter(field_name="cook_time", lookup_expr="lte")

    class Meta:
        model = Recipe
        fields = ["category", "category_id", "min_prep_time", "max_prep_time", "min_cook_time", "max_cook_time"]

    def filter_cuisines(self, qs, name, value):
        if not value:
            return qs
        parts = [p.strip() for p in value.split(",") if p.strip()]
        if not parts:
            return qs
        ids = [int(p) for p in parts if p.isdigit()]
        names = [p for p in parts if not p.isdigit()]
        q = Q()
        if ids:
            q |= Q(cuisines__id__in=ids)
        for n in names:
            q |= Q(cuisines__name__icontains=n)
        return qs.filter(q).distinct()