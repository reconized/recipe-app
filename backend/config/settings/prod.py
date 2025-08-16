from .base import * # noqa
import os
from decouple import config, Csv
import dj_database_url

DEBUG = False

if not SECRET_KEY or SECRET_KEY.startswith("dev-"):
    raise RuntimeError("SECRET_KEY must be set to a strong value in production")

# Hosts & CSRF
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# HTTPS & Security Headers
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# HSTS (one year, include subdomains, preload)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"

# --- CORS
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="", cast=Csv())

# Database
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set in production")
DATABASES["default"] = dj_database_url.parse(
    DATABASE_URL, conn_max_age=600, conn_health_checks=True
)

# Static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# DRF
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
]
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"].update({
    "anon": "30/minute",
    "user": "300/minute",
})

#  Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.security": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "django.request":  {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "axes.watch_login": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

# Content Security Policy (django-csp)
# INSTALLED_APPS += ["csp"]
# MIDDLEWARE.insert(1, "csp.middleware.CSPMiddleware")
# CSP_DEFAULT_SRC = ("'self'",)
# CSP_IMG_SRC = ("'self'", "data:", "blob:")
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
# CSP_SCRIPT_SRC = ("'self'",)
