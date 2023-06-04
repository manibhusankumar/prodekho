# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import *
from django.conf import settings
from django.contrib import messages


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        exclude = ['date_joined']

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
        user.is_active = True
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class UpdateForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput())

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'image')


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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
        'first_name', 'last_name', 'about', 'dob', 'address', 'city', 'country', 'zip_code', 'street', 'district',
        'state', 'gender')


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ('facebook', 'instagram', 'twitter', 'linkedin')


class ListingForm(forms.ModelForm):
    room_image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


    class Meta:
        model = Listing
        fields = ['title', 'type', 'price', 'category', 'keywords', 'address', 'longitude', 'latitude', 'city',
                  'email', 'phone', 'website', 'area', 'accommodation', 'yard_size', 'bedrooms', 'bathrooms',
                  'garage', 'details_text', 'wi_fi', 'pool', 'security', 'laundry_room', 'equipped_kitchen',
                  'air_conditioning', 'parking', 'room_title', 'additional_room', 'room_details', 'room_image',
                  'air_conditioner', 'tv_inside', 'ceramic_bath', 'microwave', 'video_presentation', 'video_youtube',
                  'video_vimeo', 'document', 'google_mapp', 'contact_form', 'mortage_calulator']

    # Customize form fields
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)


# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['date', 'start_time']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['date'].widget.attrs.update({'class': 'form-control'})
#         self.fields['start_time'].widget.attrs.update({'class': 'form-control'})

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['listing',  'name', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        listing = kwargs.pop('listing')
        super().__init__(*args, **kwargs)
        self.instance.listing = listing
