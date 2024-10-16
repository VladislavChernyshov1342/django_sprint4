from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'image', 'pub_date', 'location', 'is_published', 'title', 'category',)
        widgets = {
            'post': forms.DateInput(attrs={'type': 'date'})
        }
