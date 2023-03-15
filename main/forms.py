# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User
from django.conf import settings
from django.contrib import messages



class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'phone','email', 'password', 'password2')

    def is_valid(self, request):
        Email = self.data['email']
        password1 = self.data['password']
        password2 = self.data['password2']
        if User.objects.filter(email=Email).exists():
            return messages.error(request, 'email taken')
        if password1 != password2:
            # raise ValidationError("Passwords don't match")
            messages.info(request, "password did not match")
            # return redirect('taskapp:index')
        return Email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active=True
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'phone','email','image')


class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=63, widget=forms.PasswordInput)

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if len(password) < 4:
    #         messages.error(self.request, 'You are Not Login')
    #         raise ValidationError('Password must be at least 4 characters long')
    #
    #     return password

