from django import forms


# Форма авторизаци пользователя
class LoginForm(forms.Form):
    username = forms.CharField()
    # создает поле (widget=forms.PasswordInput) - элемент input с атрибутом type='password'
    password = forms.CharField(widget=forms.PasswordInput)
