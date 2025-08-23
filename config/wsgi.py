"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

# from django.core.management import call_command
# from django.contrib.auth import get_user_model
# from django.db import OperationalError

# try:
#     call_command('migrate', interactive=False)

#     User = get_user_model()
#     if not User.objects.filter(is_superuser=True).exists():
#         import os
#         username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
#         email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
#         password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'morijyobi')
#         User.objects.create_superuser(email=email, username=username,  password=password, number=2147483647)
# except OperationalError as e:
#     print('Database not ready yet:', e)
    

application = get_wsgi_application()
