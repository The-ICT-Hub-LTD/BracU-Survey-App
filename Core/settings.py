
from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = Path.joinpath(BASE_DIR, 'templates')
STATIC_DIR = Path.joinpath(BASE_DIR, 'static')
MEDIA_DIR = Path.joinpath(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gz#7qi643+%c8=v+id*t$2$_ou&*aakos+gmyc%laxn(93-9$('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECRET_KEY = config('THE_SECRET_KEY')
# DEBUG = config('WEB_DEBUG', cast = bool)

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://bracu-khabardabarcatering.up.railway.app', 
                        'http://bracu.khabardabarcatering.com',
                        'https://bracu.khabardabarcatering.com',
                        ]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'App_Survey',

    'django.contrib.sites',  
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 
    'storages',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

### Google SSO
AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.google.GoogleOAuth2', 
    'django.contrib.auth.backends.ModelBackend',  
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE' : [
            'profile',
            'email'
        ],
        'APP': {
            'client_id': '262139276381-bcoqo1v8eolsh2ma8cvnvhbb6th4q24s.apps.googleusercontent.com',
            'secret': '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',
            'key': '',
        },
        'AUTH_PARAMS': {
            'access_type':'online',
        }
    }
}

LOGIN_REDIRECT_URL = 'App_Survey:admin_dashboard' 
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'  
SOCIALACCOUNT_QUERY_EMAIL = True

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
GOOGLE_SSO_PROJECT_ID = config('GOOGLE_SSO_PROJECT_ID')
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
# SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']
# GOOGLE_SSO_ALLOWABLE_DOMAINS = ["gmail.com"]


# LOGIN_URL = 'App_Survey:admin_login'  
# LOGOUT_URL = 'App_Survey:signout'
# LOGIN_REDIRECT_URL = 'App_Survey:admin_dashboard'


# SOCIAL_AUTH_PIPELINE = (
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.auth_allowed',
#     'social_core.pipeline.social_auth.social_user',
#     'social_core.pipeline.user.get_username',
#     'App_Survey.pipeline.require_staff',        
#     'App_Survey.pipeline.create_user_profile',  
#     'App_Survey.pipeline.verify_email', 
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
# )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': 
    [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
        'DEFAULT_PERMISSION_CLASSES':
    [
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS':
    ['django_filters.rest_framework.DjangoFilterBackend']
}

ROOT_URLCONF = 'Core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Core.wsgi.application'

# AUTH_USER_MODEL = 'App_Customer.CustomUser'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# POSTGRESQL ##
DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'vBcwWvGjRtFtwiJjQwEXJuQNCGtFpoEn',
        'HOST': 'autorack.proxy.rlwy.net',
        'PORT': '42463',
    }
}

# ## MYSQL ##
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'khabardabarcater_bracu',
#         'USER': 'khabardabarcater_khabardabar',
#         'PASSWORD': '$iLoveKhabardabar@100%',
#         'HOST':'127.0.0.1',
#         'PORT':'3306',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# STATIC_ROOT = ''

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = MEDIA_DIR

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'App_Survey.UserProfile'

# LOGIN_URL = '/signin/'

# LOGIN_REDIRECT_URL = 'App_Survey/admin-login'
# LOGOUT_REDIRECT_URL = 'App_Survey/signout'

# from datetime import timedelta
# AUTO_LOGOUT = {
#     'IDLE_TIME': timedelta(minutes=30),
#     #  'SESSION_TIME': timedelta(minutes=30),
#     'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
#      'MESSAGE': 'The session has expired. Please login again to continue.',
# }


# # Send Mail 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = 'khabardabarcateringbd@gmail.com'
EMAIL_HOST_PASSWORD = 'icpmukqvkqogytdu'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ### Lockdown Password
# LOCKDOWN_PASSWORDS = ('letmein', 'beta')


### Cross Site Scripting 
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

### Redirects all non-HTTPS requests to HTTP
# SECURE_SSL_REDIRECT = True

### HTTP Strict Transport Security
# SECURE_HSTS_SECONDS = 86400
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

### Cross-site request forgery(CSRF) protection
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


# S3 BUCKETS CONFIG start

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")  


STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None


STORAGES = {

    # Media file (image) management   
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
    
    # CSS and JS file management
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}
