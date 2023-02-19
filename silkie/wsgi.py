"""
WSGI config for jscoq project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/afs/qatar.cmu.edu/course/15/logic/silkie')
sys.path.append('/afs/qatar.cmu.edu/course/15/logic/silkie/silkie')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'silkie.settings')

application = get_wsgi_application()
