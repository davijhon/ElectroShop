import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')

from dj_static import Cling # para static file

application = Cling(get_wsgi_application())