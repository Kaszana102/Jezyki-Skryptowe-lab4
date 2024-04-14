from django import forms
from django.forms import ModelForm

from .models import *


class RegisterForm(forms.Form):
    nick = forms.CharField(max_length=255)
    mail = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)


class LoginForm(forms.Form):
    mail = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)


class UpdateImageForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    imageID = forms.IntegerField(widget=forms.HiddenInput())
    type = forms.CharField(widget=forms.HiddenInput(),  initial="update")



class PublishForm(ModelForm):
    class Meta:
        model = Image
        fields = ["title", "description", "image"]
