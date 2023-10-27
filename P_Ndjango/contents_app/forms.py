from django import forms
from .models import Board
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    post_content = forms.CharField(
        widget=SummernoteWidget(),
    )

    class Meta:
        model = Board
        fields = ["post_title", "post_content", "board_no"]
        widgets = {
            " ": SummernoteWidget(),
        }
        exclude = [
            "post_time",
            "post_like",
            "post_hit",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
