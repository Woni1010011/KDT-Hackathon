# Generated by Django 4.2.5 on 2023-11-01 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0005_alter_user_user_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userigrd',
            name='ingredients_igrd_no',
        ),
        migrations.RemoveField(
            model_name='userigrd',
            name='user_no',
        ),
    ]
