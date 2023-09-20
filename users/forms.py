from django import forms
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
from .models import CustomUser


class NewuserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password1', 'password2']


class EdituserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"