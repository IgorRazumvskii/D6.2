# Generated by Django 4.2 on 2023-07-27 09:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_category_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='get_subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]