from django.db import models

# Create your models here.

class User(models.Model):
    user_no = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=100, unique=True)
    user_password = models.CharField(max_length=200)
    user_email = models.CharField(max_length=100)
    user_name = models.CharField(max_length=20)
    user_nick = models.CharField(max_length=50, blank=True, null=True)
    user_phone = models.CharField(max_length=11)
    user_address = models.CharField(max_length=200, blank=True, null=True)
    sub_date = models.DateTimeField(auto_now_add=True)
    user_point = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.user_id