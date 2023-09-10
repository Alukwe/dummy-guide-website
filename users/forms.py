from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile, ProfilePicture

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields = ['picture']