from django.db import models
from contents_app.models import Ingredients


# Create your models here.

class User(models.Model):
    user_no = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=150, unique=True)
    user_password = models.CharField(max_length=200)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=200, unique=True)
    user_nick = models.CharField(max_length=50, unique=True)
    user_phone = models.CharField(max_length=11)
    user_address = models.CharField(max_length=200)
    sub_date = models.DateTimeField(auto_now_add=True)
    user_point = models.IntegerField(default=0)

    def __str__(self):
        return self.user_id
    
class UserIgrd(models.Model):
    ingredients_igrd_no = models.ForeignKey(Ingredients, on_delete=models.CASCADE, related_name="related_user_igrds")
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_no_info")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id_info")
    igrd_name = models.CharField(max_length=255)
    user_igrd_date = models.DateField()
    exp_date = models.DateField()

    def __str__(self):
        return self.igrd_name