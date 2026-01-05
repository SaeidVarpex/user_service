from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
# بقیه از env لود می‌شن
