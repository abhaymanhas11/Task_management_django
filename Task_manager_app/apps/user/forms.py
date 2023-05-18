from django import forms
from apps.user.models import User


class RegisterUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
