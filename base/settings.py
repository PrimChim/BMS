from pathlib import Path
import os

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'knox',
    'billing',
    'corsheaders',
    'compressor',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'users/static')
]

STATIC_ROOT = BASE_DIR / 'static'

#==================Compress settings==================#
COMPRESS_ROOT = BASE_DIR / 'static'
 
COMPRESS_ENABLED = True
 
STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'base/templates')],
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

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL to redirect to after logout to users:login
LOGOUT_REDIRECT_URL = '/login'

# URL to redirect to login page
LOGIN_URL = '/login'

#==================jaxmin settings==================#
JAZMIN_SETTINGS = {
    "site_title": "Billing System",
    "site_header": "Billing System",
    "site_logo": "static/users/logo/1.png",
    "welcome_sign": "Welcome to Khata",
    "copyright": "Khata",
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "related_modal_active": False,
    "navigation_expanded": True,
    "navigation_collapsed": False,
    "site_style": "sidebar",
    "top_navbar": True,
    "show_apps": True,
    "related_modal_active": False,
    "show_user_actions": True,
    "user_menu": [
        {"name": "Change Password", "url": "admin:password_change"},
        {"name": "Logout", "url": "users:logout_api"},
    ],
    "show_app_list": True,
    "app_list": [
        {"name": "Users", "icon": "fas fa-users", "models": [
            {"name": "User", "icon": "fas fa-user", "url": "admin:users_user_changelist"},
            {"name": "Profile", "icon": "fas fa-user", "url": "admin:users_profile_changelist"},
        ]},
        {"name": "Billing", "icon": "fas fa-money-bill", "models": [
            {"name": "Invoice", "icon": "fas fa-file-invoice", "url": "admin:billing_invoice_changelist"},
            {"name": "Payment", "icon": "fas fa-money-check", "url": "admin:billing_payment_changelist"},
        ]},
    ],
}

#==================email settings==================#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')