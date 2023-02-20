from django import forms
from django.forms import ModelForm
from .models import Village, User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class VillageForm(ModelForm):
    class Meta:
        model = Village
        fields = '__all__'
        exclude = ['host', 'sophists']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

        def clean_email(self):
            data = self.cleaned_data['email']
            domain = data.split('@')[1]
            domain_list = ["georgebrown.ca"]
            if domain not in domain_list:
                raise forms.ValidationError(
                    "Please enter a George Brown Email Address with a valid domain")
            return data

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
            return user
