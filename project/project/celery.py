import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')


class Config:

    REDIS_HOST = '127.0.0.1'  # NOT 0.0.0.0 with docker
    REDIS_PORT = '6379'
    BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
    RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
    ACCEPT_CONTENT = ['application/json']
    TASK_SERIALIZER = 'json'
    RESULT_SERIALIZER = 'json'


app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
#app.config_from_object(Config)
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'name': {
        'task': 'news.tasks.my_job',
        'schedule': crontab(hour='8', minute='0', day_of_week='1')
    }
}
