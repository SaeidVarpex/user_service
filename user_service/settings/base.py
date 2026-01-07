import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# مسیر پایه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# کلید امنیتی - حتماً در production از یک مقدار قوی و محرمانه استفاده کن
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-change-this-in-production-to-a-strong-random-value'
)

# حالت دیباگ - در production حتماً False باشه
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# هاست‌های مجاز
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# اپلیکیشن‌های نصب‌شده
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # پکیج‌های ثالث
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # اپ‌های محلی
    'users',
    'authentication',
]

# میدلورها
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL اصلی
ROOT_URLCONF = 'user_service.urls'

# تنظیمات قالب‌ها (برای ادمین و ایمیل‌های داخلی)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# WSGI application
WSGI_APPLICATION = 'user_service.wsgi.application'

# دیتابیس - از متغیرهای محیطی استفاده می‌کنه
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# اعتبارسنجی رمز عبور
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# مدل کاربر سفارشی
AUTH_USER_MODEL = 'users.CustomUser'

# زبان و زمان
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# فایل‌های استاتیک و مدیا
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# مقدار پیش‌فرض فیلدهای auto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# تنظیمات Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
}

# تنظیمات Simple JWT
"""SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}"""

#import os
#from pathlib import Path

#BASE_DIR = Path(__file__).resolve().parent.parent

JWT_KEYS_DIR = BASE_DIR / "user_service" / "jwt_keys"

# مسیر کلیدهای production
PROD_PRIVATE_KEY = JWT_KEYS_DIR / "prod_private.pem"
PROD_PUBLIC_KEY = JWT_KEYS_DIR / "prod_public.pem"

# مسیر کلیدهای development
DEV_PRIVATE_KEY = JWT_KEYS_DIR / "dev_private.pem"
DEV_PUBLIC_KEY = JWT_KEYS_DIR / "dev_public.pem"


def read_key(path: Path) -> str | None:
    if path.exists():
        return path.read_text()
    return None


# انتخاب کلیدها
SIGNING_KEY = read_key(PROD_PRIVATE_KEY) or read_key(DEV_PRIVATE_KEY)
VERIFYING_KEY = read_key(PROD_PUBLIC_KEY) or read_key(DEV_PUBLIC_KEY)

if not SIGNING_KEY or not VERIFYING_KEY:
    raise RuntimeError("JWT keys are missing. No valid key pair found.")


SIMPLE_JWT = {
    "ALGORITHM": "RS256",
    "SIGNING_KEY": SIGNING_KEY,
    "VERIFYING_KEY": VERIFYING_KEY,

    # پیشنهاد حرفه‌ای
    "ISSUER": "user-service",
    "AUDIENCE": "api-gateway",

    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# امنیت اضافی (در prod مهم‌تره)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# لاگینگ پایه (در prod می‌تونی پیشرفته‌تر کنی)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
