"""
WSGI config for jobsaccess project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os, sys
sys.path.append('/home/tristan/jobsaccess')
sys.path.append('/home/tristan/jobsaccess/jobsaccess/lib/python2.7/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobsaccess.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
