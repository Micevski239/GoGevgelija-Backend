import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
import logging.config

BASE_DIR = Path(__file__).resolve().parent.parent

# -------- Runtime flags
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if os.getenv("DJANGO_DEBUG", "0") == "1":
        SECRET_KEY = "dev-only-do-not-use-in-prod"
    else:
        raise ValueError("DJANGO_SECRET_KEY environment variable must be set in production")

DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

DEFAULT_IP = "167.71.37.168"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    f"localhost,127.0.0.1,{DEFAULT_IP},gogevgelija.com,www.gogevgelija.com,admin.gogevgelija.com"
).split(",")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://gogevgelija.com,https://www.gogevgelija.com,https://admin.gogevgelija.com,http://167.71.37.168"
).split(",")

# -------- Security settings
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Additional security headers for production
if not DEBUG:
    SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000"))  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", "1") == "1"
    SECURE_HSTS_PRELOAD = os.getenv("DJANGO_SECURE_HSTS_PRELOAD", "1") == "1"
    SECURE_REFERRER_POLICY = os.getenv("DJANGO_SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin")
    
# Cookie security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Frame options
X_FRAME_OPTIONS = 'DENY'

# -------- Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "modeltranslation",
    "core.apps.CoreConfig",
]

# -------- Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"

# -------- Database
db_url = os.getenv("DATABASE_URL", "sqlite:///" + str(BASE_DIR / "db.sqlite3"))

# DigitalOcean Managed Database always requires SSL
ssl_require = not DEBUG and 'sqlite' not in db_url.lower()

DATABASES = {
    "default": dj_database_url.parse(
        db_url, 
        conn_max_age=600, 
        ssl_require=ssl_require,
        conn_health_checks=True  # Enable connection health checks
    )
}

# Additional SSL settings for DigitalOcean Managed Database
if not DEBUG and 'postgres' in db_url.lower():
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
        'sslcert': None,  # DO managed DB handles SSL automatically
        'sslkey': None,
        'sslrootcert': None,
    }

# -------- DRF / Auth
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", "15"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME_DAYS", "7"))),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": os.getenv("JWT_ROTATE_REFRESH_TOKENS", "1") == "1",
    "BLACKLIST_AFTER_ROTATION": os.getenv("JWT_BLACKLIST_AFTER_ROTATION", "1") == "1",
}

# -------- Static
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "core" / "static",
]
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

# -------- CORS
# Default: allow common origins. Set CORS_ALLOWED_ORIGINS in env for production.
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "0") == "1"
if not CORS_ALLOW_ALL_ORIGINS:
    _cors_env = os.getenv("CORS_ALLOWED_ORIGINS", "https://admin.gogevgelija.com,https://gogevgelija.com,https://www.gogevgelija.com")
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_env.split(",") if o.strip()]

# -------- Security / proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Enable SSL redirect for production (when not in DEBUG mode)
SECURE_SSL_REDIRECT = not DEBUG and os.getenv("DJANGO_SECURE_SSL_REDIRECT", "1") == "1"

# -------- i18n
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('mk', 'Macedonian'),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------- Admin Security
ADMIN_ENABLED = os.getenv("DJANGO_ADMIN_ENABLED", "1" if DEBUG else "0") == "1"

# -------- Rate Limiting & Performance
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv("DJANGO_DATA_UPLOAD_MAX_MEMORY_SIZE", "5242880"))  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv("DJANGO_FILE_UPLOAD_MAX_MEMORY_SIZE", "5242880"))  # 5MB

# -------- Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_errors.log'),
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple' if DEBUG else 'verbose',
        },
        'security': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'security.log'),
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'] if not DEBUG else ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'security'] if not DEBUG else ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {  # Your app logs
            'handlers': ['console', 'file'] if not DEBUG else ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Ensure logs directory exists
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# -------- Error Monitoring
# Add Sentry or similar service configuration
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN and not DEBUG:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), sentry_logging],
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
        send_default_pii=False,
        environment=os.getenv("ENVIRONMENT", "production"),
    )

# -------- Health Check Settings
HEALTH_CHECK_ENABLED = os.getenv("HEALTH_CHECK_ENABLED", "1") == "1"

# -------- Email Configuration (for error notifications)
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', '1') == '1'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@gogevgelija.com')
    
    # Admin email notifications
    ADMINS = [
        ('Admin', os.getenv('ADMIN_EMAIL', 'admin@gogevgelija.com')),
    ]
    MANAGERS = ADMINS
    
    # Email admin on errors
    LOGGING['handlers']['mail_admins'] = {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler',
        'include_html': True,
    }
    LOGGING['loggers']['django']['handlers'].append('mail_admins')

# -------- Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache' if os.getenv('REDIS_URL') else 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': os.getenv('REDIS_URL', 'unique-snowflake'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        } if os.getenv('REDIS_URL') else {},
        'KEY_PREFIX': 'gogevgelija',
        'TIMEOUT': 300,
    }
}

# -------- Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache' if os.getenv('REDIS_URL') else 'django.contrib.sessions.backends.db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE', '1209600'))  # 2 weeks