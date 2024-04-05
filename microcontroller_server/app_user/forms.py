from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

# Obtiene user por defecto
User = get_user_model()

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'Email',
            'password': 'Password',
        }