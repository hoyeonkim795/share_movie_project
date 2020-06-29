from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm) :
    class Meta():
        model = get_user_model()
        fields = {'image', 'myinfo'}


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()