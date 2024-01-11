from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import *


class SignUpForm(UserCreationForm):
    group_choices = [("User", "User"), ("Admin", "Admin")]
    group = forms.ChoiceField(choices=group_choices)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        group_name = self.cleaned_data["group"]
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class CreateChannelForm(forms.Form):
    Name = forms.CharField(max_length=50)
    Description = forms.CharField(max_length=200)


class UpdateChannelForm(forms.Form):
    Name = forms.CharField(max_length=50, required=False)
    Description = forms.CharField(max_length=200, required=False)
    SAFE_MODE_CHOICES = [
        ("Disabled", "Disabled"),
        ("Enabled", "Enabled"),
    ]
    SafeMode = forms.ChoiceField(choices=SAFE_MODE_CHOICES, required=False)


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["profile_picture"]
