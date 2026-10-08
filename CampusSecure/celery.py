import os
from celery import Celery

# setup celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CampusSecure.settings')

app = Celery("CampusSecure")
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks()


