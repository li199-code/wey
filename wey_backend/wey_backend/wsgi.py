"""
WSGI config for wey_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wey_backend.settings')
if os.environ.get('DJANGO_ENV') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wey_backend.settings_prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wey_backend.settings_dev')

application = get_wsgi_application()
