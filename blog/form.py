from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


# Форма модели - динамически генерируемая
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # по умолчанию форма берет все поля модели
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()
