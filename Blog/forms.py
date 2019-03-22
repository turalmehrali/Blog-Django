
from django import forms
from .models import Article, Comment, Reply

class Articleform(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'article_category', 'content', 'article_image', 'draft']


class CommentForm(forms.ModelForm):


    class Meta:
        model = Comment
        fields = ['comment_content']

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['reply_content']



