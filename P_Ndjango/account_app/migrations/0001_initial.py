# Generated by Django 4.2.5 on 2023-10-24 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contents_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=150, unique=True)),
                ('user_password', models.CharField(max_length=200)),
                ('user_name', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=200, unique=True)),
                ('user_nick', models.CharField(max_length=50, unique=True)),
                ('user_phone', models.CharField(max_length=11)),
                ('user_address', models.CharField(max_length=200)),
                ('sub_date', models.DateTimeField(auto_now_add=True)),
                ('user_point', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserIgrd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('igrd_name', models.CharField(max_length=255)),
                ('user_igrd_date', models.DateField()),
                ('ingredients_igrd_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_user_igrds', to='contents_app.ingredients')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id_info', to='account_app.user')),
                ('user_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_no_info', to='account_app.user')),
            ],
        ),
    ]
