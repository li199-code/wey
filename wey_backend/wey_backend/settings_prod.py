
from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

WEBSITE_URL = 'http://1.116.161.57:8000' # 后端服务url,用于静态资源请求


## 前端网址，用于跨域白名单
CORS_ALLOWED_ORIGINS = [
    "http://1.116.161.57:8080",
]

CSRF_TRUSTED_ORIGINS = ["http://1.116.161.57:8000"]


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wey',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = '/var/www/mysite/assets/static'
MEDIA_URL = 'media/'
MEDIA_ROOT = '/var/www/mysite/assets/media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


