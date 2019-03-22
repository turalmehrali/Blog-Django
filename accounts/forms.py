
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
#from django.db import models
from .models import UserProfile, UserType

class SignUpForm(UserCreationForm):
    USERTYPES = (
        (1, 'oxuyucu'),
        (2, 'yazar'),
    )
    user_type = forms.ChoiceField(required=True, label='Hesab növü', choices=USERTYPES)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'user_type', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}




class UserForm(forms.ModelForm):
    USERTYPES = (
        (1, 'oxuyucu'),
        (2, 'yazar'),
    )

    bio = forms.CharField(widget=forms.Textarea, max_length=2000, label='Bioqrafiya')
    #profile_photo = forms.ImageField(label='Profil rəsmi')
    #user_type = forms.ChoiceField(required=True, label='Hesab növü', choices=USERTYPES)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio']#, 'profile_photo','user_type']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

        self.fields['bio'].widget.attrs['rows'] = 10
        self.fields['bio'].widget.attrs['cols'] = 10


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_photo']

