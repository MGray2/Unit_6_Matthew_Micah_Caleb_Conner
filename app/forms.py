from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class SignUpForm(UserCreationForm):
    group_choices = [("User", "User"), ("Admin", "Admin")]
    group = forms.ChoiceField(choices=group_choices)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        group_name = self.cleaned_data["group"]
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
