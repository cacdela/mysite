from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Profile
import re


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(label='ФИО', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Введите ФИО'}), required=True)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Введите email'}))
    agree_to_process_personal_data = forms.BooleanField(label='Согласие на обработку персональных данных',required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        if not re.match('^[а-яА-ЯёЁ\s-]+$', full_name):
            raise ValidationError(_('ФИО может содержать только кириллические буквы, дефис и пробелы'))

        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not all(char.isalnum() or char == '-' for char in username):
            raise ValidationError(_('Логин может содержать только латиницу и дефис'))

        if User.objects.filter(username=username).exists():
            raise ValidationError(_('Этот логин уже занят'))

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError(_('Этот email уже занят'))

        return email

    def clean_agree_to_process_personal_data(self):
        agree_to_process_personal_data = self.cleaned_data.get('agree_to_process_personal_data')

        if not agree_to_process_personal_data:
            raise ValidationError(get_language('Вы должны дать согласие на обработку персональных данных'))

        return agree_to_process_personal_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
