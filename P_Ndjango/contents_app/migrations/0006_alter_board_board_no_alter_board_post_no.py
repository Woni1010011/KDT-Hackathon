# Generated by Django 4.2.5 on 2023-10-26 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents_app', '0005_delete_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='board_no',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='board',
            name='post_no',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
