from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-input',
        'autocomplete': 'username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-input',
        'autocomplete': 'current-password',
    }))


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'First name',
        'class': 'form-input',
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Last name',
        'class': 'form-input',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'class': 'form-input',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Choose a username',
        'class': 'form-input',
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Create password',
        'class': 'form-input',
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'form-input',
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
