# Generated by Django 5.1.5 on 2025-02-23 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_shopkeeperrequest_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('brand', 'Brand'), ('shopkeeper', 'Shopkeeper'), ('user', 'User')], default='user', max_length=15),
        ),
    ]
