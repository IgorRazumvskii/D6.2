from project.celery import app
from celery import shared_task

import datetime

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail
from .models import Post, PostCategory, Category


@shared_task
def task_send_mail(subscribers, instance, url):

    for mail, username in subscribers:
        send_mail(
            f"{username}, прочитайте новую статью по вашей подписки",
            f'{instance}: {url}',
            'razumovskijigor6@gmail.com',
            [mail],
            fail_silently=False
        )


@shared_task()
def my_job():
    #  Your job processing logic here...
    categories = Category.objects.all()
    for c in categories:
        print(c)

        posts = Post.objects.filter(
            category=c,
            date_and_time__gt=datetime.datetime.today().astimezone() - datetime.timedelta(days=7)
        )
        #  subscribers = User.objects.filter(get_subscribers__in=posts[0].category.all())
        if len(posts) == 0:
            continue
        subscribers = posts[0].category.values('subscribers__email', 'subscribers__username')
        headers = []
        for p in posts:
            print(p.date_and_time)
            headers.append(p.header + " " + 'http://127.0.0.1:8000' + p.get_absolute_url())

        for mail in subscribers:
            send_mail(
                f"{mail['subscribers__username']}, прочитайте новую статью по вашей подписки",
                "\n".join(headers),
                from_email='razumovskijigor6@gmail.com',
                recipient_list=[mail['subscribers__email']],
            )