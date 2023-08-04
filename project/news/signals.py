from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post, PostCategory, Category
from django.contrib.auth.models import User


@receiver([post_save, m2m_changed], sender=PostCategory)
def subscribe(sender, instance, **kwargs):
    cat = PostCategory.objects.get(post=instance).category
    print(cat)
    #subscribers = User.objects.filter(get_subscribers__in=instance.category.all())
    subscribers = PostCategory.objects.get(post=instance).category.subscribers
    mails = [i.email for i in subscribers]
    print(subscribers)

