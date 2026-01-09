from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h9l2xi5jfz_^jnz^p*yg43uqon$&p#=u7)d4+6-zr_&nf3g2^9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.100.22', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    'corsheaders',
    'users',
    'disease',
    'sensors',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOWED_ORIGINS=[
    'http://localhost:5173',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

AUTH_USER_MODEL = 'users.CustomUser'
ROOT_URLCONF = 'agriboost.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'agriboost.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # default
]
CORS_ALLOW_CREDENTIALS = True

# Optional: path to disease model, can be overridden via environment variable
DISEASE_MODEL_PATH = os.environ.get(
    "DISEASE_MODEL_PATH",
    str(BASE_DIR / "disease" / "sugarcane_leaf_cnn_model.h5"),
)

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),   # Access token valid for 12 hours
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),   # Refresh token valid for 30 days
    "ROTATE_REFRESH_TOKENS": True,                  # Get a new refresh token each time
    "BLACKLIST_AFTER_ROTATION": True,               # Old refresh tokens go to DB blacklist
    "AUTH_HEADER_TYPES": ("Bearer",),
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "AgriBoost <noreply@agriboost.com>"

# Firebase Realtime Database Configuration
# TODO: Add your Firebase Admin SDK credentials to backend/firebase_key.json
# Download the service account key from Firebase Console:
# 1. Go to Firebase Console > Project Settings > Service Accounts
# 2. Click "Generate New Private Key"
# 3. Save the JSON file as backend/firebase_key.json
FIREBASE_DATABASE_URL = "https://agriboost-fyp-default-rtdb.asia-southeast1.firebasedatabase.app/"
FIREBASE_KEY_FILE = str(BASE_DIR / "firebase_key.json")
FIREBASE_SENSORS_PATH = "/IoT_Sensors"  # Data is at root level, not under /sensors