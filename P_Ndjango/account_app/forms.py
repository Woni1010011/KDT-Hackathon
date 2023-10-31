from django import forms
from .models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["user_nick", "user_email", "user_address", "user_name", "user_phone", "user_img"]
