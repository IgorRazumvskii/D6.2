import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, PostCategory, Category
from django.contrib.auth.models import User

from django.core.mail import send_mail
import datetime

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
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



# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")