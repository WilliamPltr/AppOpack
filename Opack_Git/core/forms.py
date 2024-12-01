from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Adresse mail",
        widget=forms.EmailInput(attrs={
            'class': 'peer block w-full rounded-lg border border-gray-300 bg-white px-4 pt-5 pb-2 text-sm text-gray-900 focus:border-primary focus:ring-2 focus:ring-primary focus:outline-none',
            'placeholder': ' ',
        }),
        error_messages={
            'required': '🌟 Merci de saisir une adresse mail.',
            'invalid': '💌 Veuillez entrer une adresse mail valide.',
        }
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'peer block w-full rounded-lg border border-gray-300 bg-white px-4 pt-5 pb-2 text-sm text-gray-900 focus:border-primary focus:ring-2 focus:ring-primary focus:outline-none',
            'placeholder': ' ',
        }),
        error_messages={
            'required': '🔒 Merci de saisir votre mot de passe.',
        }
    )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'peer block w-full rounded-lg border border-gray-300 bg-white px-4 pt-5 pb-2 text-sm text-gray-900 focus:border-primary focus:ring-2 focus:ring-primary focus:outline-none',
            'placeholder': ' ',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
