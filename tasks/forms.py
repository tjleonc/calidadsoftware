# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        max_length=254,
        help_text='Requerido. Ingresa un correo electrónico válido.'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica si el email ya está registrado
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email
    

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']  # Campos que se mostrarán en el formulario