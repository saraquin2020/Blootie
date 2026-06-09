from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg rounded-4', 'placeholder': 'Escribe tu usuario'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg rounded-4', 'placeholder': 'Escribe tu contraseña'})
    )
