from django import forms
from .models import User


class UserEditForm(forms.ModelForm):
    user_name = forms.CharField(max_length=100)
    user_email = forms.EmailField(max_length=200)
    user_nick = forms.CharField(max_length=50)
    user_phone = forms.CharField(max_length=11)
    user_address = forms.CharField(max_length=200)
    user_img = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["user_nick", "user_email", "user_address", "user_name", "user_phone", "user_img"]
