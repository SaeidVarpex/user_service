from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = BASE_DIR / 'db.sqlite3'
