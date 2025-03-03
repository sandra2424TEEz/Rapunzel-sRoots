# Generated by Django 5.1.5 on 2025-03-01 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('shopkeeper', 'Shopkeeper'), ('user', 'User')], default='user', max_length=15),
        ),
    ]
