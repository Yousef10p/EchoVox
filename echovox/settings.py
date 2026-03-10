import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production-123')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Railway Domain Fix
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'echovox.up.railway.app,127.0.0.1,localhost').split(',')

CSRF_TRUSTED_ORIGINS = [
    "https://echovox.up.railway.app",
    "https://*.127.0.0.1"
]

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    # 1. CORE DJANGO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Keep this here
    
    # 2. MEDIA STORAGE (Must be BELOW staticfiles to avoid collection conflicts)
    'cloudinary_storage',
    'cloudinary',
    
    # 3. YOUR APPS
    'apps.core',
    'apps.accounts',
    'apps.translators',
    'apps.dashboard',
    'apps.translate',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # MUST BE SECOND
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'echovox.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'apps' / 'templates'], # Added base templates path
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', # Added for Cloudinary
            ],
        },
    },
]

WSGI_APPLICATION = 'echovox.wsgi.application'

# --- DATABASE ---
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# --- STATIC & MEDIA FILES (THE FIX) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Django 4.2+ Storage Logic
if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.StaticFilesStorage",
        },
    }
    WHITENOISE_MANIFEST_STRICT = False
else:
    STORAGES = {
        "default": { "BACKEND": "django.core.files.storage.FileSystemStorage" },
        "staticfiles": { "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage" },
    }

# Cloudinary Credentials
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# --- AUTHENTICATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# --- AI & UPLOAD CONFIG ---
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
ASSEMBLY_AI_KEY = os.getenv('ASSEMBLY_AI_KEY', '')

FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024 
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

# --- DEBUG PRINTS (Optional for logs) ---
print(f"DEBUG: BASE_DIR is {BASE_DIR}")
print(f"DEBUG: Static folder is {BASE_DIR / 'static'}")