"""
WSGI config for OvernightWeb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
from whitenoise.django import DjangoWhiteNoise



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OvernightWeb.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
