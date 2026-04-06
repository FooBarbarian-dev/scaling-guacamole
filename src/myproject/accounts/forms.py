"""Authentication forms."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    """Custom login form with styled widgets."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Username"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input", "placeholder": "Password"}),
    )


class RegistrationForm(UserCreationForm):
    """User registration form."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-input", "placeholder": "Email"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-input", "placeholder": "Username"}),
        }
