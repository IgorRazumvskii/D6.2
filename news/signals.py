from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail
from .models import Post, PostCategory, Category
from django.contrib.auth.models import User
from .tasks import task_send_mail

#  Реализовано в таске
'''
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        subscribers = instance.category.values('subscribers__email', 'subscribers__username')
        url = 'http://127.0.0.1:8000' + instance.get_absolute_url()
        print(subscribers)
        for mail in subscribers:
            send_mail(
                f"{mail['subscribers__username']}, прочитайте новую статью по вашей подписки",
                f'{instance.header}: {url}',
                'razumovskijigor6@gmail.com',
                [mail['subscribers__email']],
                fail_silently=False
            )
'''


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        subscribers = instance.category.values('subscribers__email', 'subscribers__username')
        url = 'http://127.0.0.1:8000' + instance.get_absolute_url()
        print(subscribers)
        l_sub = []
        for sub in subscribers:
            l_sub.append([sub['subscribers__email'], sub['subscribers__username']])

        task_send_mail.delay(l_sub, instance.header, url)
