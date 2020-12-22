from django import forms
from django.utils.safestring import mark_safe

from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    # content = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
    content = forms.CharField(label=mark_safe("What's on your mind..."),widget=forms.Textarea(attrs={'rows':7}))

    class Meta:
        model = Post
        fields = ('content', 'image')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ('body',)
