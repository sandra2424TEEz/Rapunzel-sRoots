# Generated by Django 5.1.5 on 2025-02-12 11:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_cartitem_quantity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shopkeeperrequest',
            unique_together={('user', 'product_name')},
        ),
    ]
