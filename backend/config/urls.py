"""
URL configuration for recipe project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    # Admin URLs
    path("admin/", admin.site.urls),

    # App API
    path("api/", include("apps.recipes.urls", namespace="recipes")),

    # OpenAPI / Docs URLs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", RedirectView.as_view(url="/docs/", permanent=False)),

    # Auth Djoser + JWT URLs
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Token Blacklist
    path('auth/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
