from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import ContactMessage, UserProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if UserProfile.objects.filter(phone__iexact=phone).exists():
            raise forms.ValidationError('This phone number is already registered.')
        return phone


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username / Email / Phone')


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'phone', 'subject', 'message')
