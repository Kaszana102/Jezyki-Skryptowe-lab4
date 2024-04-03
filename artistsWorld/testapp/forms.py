from django import forms
from django.forms import ModelForm

from .models import User,Image


class RegisterForm(forms.Form):
    nick = forms.CharField(max_length=255)
    mail = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

class LoginForm(forms.Form):
    mail = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)


class PublishForm(ModelForm):
    class Meta:
        model = Image
        fields = ["title", "description", "image"]