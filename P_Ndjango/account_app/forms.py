from django import forms
from .models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "user_name",
            "user_email",
            "user_nick",
            "user_phone",
            "user_address",
            "user_point",
            "user_img",
            "user_point",
        ]


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
