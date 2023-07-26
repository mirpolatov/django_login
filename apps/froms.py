from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, EmailField, Form

from apps.models import User


class RegisterForm(ModelForm):
    confirm_password = CharField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

    def clean_password(self):
        if self.cleaned_data['password'] != self.data['confirm_password']:
            raise ValidationError('Password didn\'t match ')
        return make_password(self.cleaned_data['password'])


class CustomLoginForm(Form):
    email = EmailField()
    password = CharField()
