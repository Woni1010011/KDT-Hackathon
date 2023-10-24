from django import forms
from .models import Board
from django_summernote.widgets import SummernoteWidget

# class PostForm(forms.ModelForm):
#     content = forms.CharField(widget=SummernoteWidget())
#     topic = forms.ModelChoiceField(
#         queryset=Topic.objects.all(),
#         widget=forms.RadioSelect,
#         to_field_name='name',
#         initial = '일상'
#     )
#     class Meta:
#         model = BlogPost
#         fields = ['title', 'content', 'topic']


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Board
        fields = ['board_no','post_no','post_title', 'post_content', 'user_nick', 'post_time', 'post_like']
        widgets = {
            'content': SummernoteWidget(),
        }
        exclude = ['author', 'created_at', 'updated_at', 'is_draft']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        