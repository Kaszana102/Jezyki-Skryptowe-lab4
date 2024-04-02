from django import forms


class RegisterForm(forms.Form):
    nick = forms.CharField(max_length=255)
    mail = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

class LoginForm(forms.Form):
    mail = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
class PublishForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    image = forms.ImageField()
