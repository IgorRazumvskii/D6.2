from django.core.mail import send_mail
from project.celery import app


@app.task
def send():
    send_mail(
        'Theme',
        'Text',
        'razumovskijigor6@gmail.com',
        ['igor.raz@list.ru', ], fail_silently=False
        )


@app.task
def second_send():
    send_mail(
        'Theme',
        'Text',
        'razumovskijigor6@gmail.com',
        ['igor.raz@list.ru', ], fail_silently=False
        )
#  bogomolovog@email.ru

@app.task
def task(x, y):
    return x+y


@app.task(bind=True, default_retry_delay=60)
def func(self, x, y):
    try:
        return x+y
    except Exception as ex:
        raise self.retry(exc=ex, countdown=60)
