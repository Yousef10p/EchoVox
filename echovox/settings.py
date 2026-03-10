import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-echovox-change-in-production-xyz123')

# DEBUG is True locally, False on Railway
DEBUG = os.getenv('DEBUG', 'True') == 'True'


CSRF_TRUSTED_ORIGINS = [
    "https://echovox.up.railway.app",
    "https://*.127.0.0.1"
]



# On Railway, set ALLOWED_HOSTS to "your-app.up.railway.app"
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Media Storage (Must be before staticfiles)
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    # Your Apps
    'apps.core',
    'apps.accounts',
    'apps.translators',
    'apps.dashboard',
    'apps.translate',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must be right below SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware', 
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
        'DIRS': [
            BASE_DIR / 'apps' / 'templates',
            BASE_DIR / 'apps' / 'core' / 'templates',
            BASE_DIR / 'apps' / 'accounts' / 'templates',
            BASE_DIR / 'apps' / 'translators' / 'templates',
            BASE_DIR / 'apps' / 'translate' / 'templates',
            BASE_DIR / 'apps' / 'dashboard' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'echovox.wsgi.application'

# --- DATABASE ---
# Uses Postgres on Railway, SQLite locally
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# --- STATIC FILES (WhiteNoise) ---
STATIC_URL = '/static/'
_STATIC_DIR = BASE_DIR / 'static'
STATICFILES_DIRS = [_STATIC_DIR] if _STATIC_DIR.exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Enable compression and caching for production
if not DEBUG:
    # Use the base storage to avoid compression-related FileNotFoundError crashes
    STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
    # Extra safety: tell WhiteNoise not to panic if a file is missing
    WHITENOISE_MANIFEST_STRICT = False

# --- MEDIA FILES (Cloudinary) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

if not DEBUG:
    # Use Cloudinary in production (Railway storage is not persistent)
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Use local storage for development
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

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