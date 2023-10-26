from django import forms
from .models import Write_post
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=SummernoteWidget(),
    )

    class Meta:
        model = Write_post
        fields = []
        widgets = {
            " ": SummernoteWidget(),
        }
        exclude = [
            "post_time",
            "post_like",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
