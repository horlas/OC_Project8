from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth.forms import AuthenticationForm


# class CreateUserForm(PopRequestMixin, CreateUpdateAjaxMixin, ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#         widgets = {
#
#             'username': TextInput(attrs={'class': 'form-control'}) ,
#             'email': EmailInput(attrs={'class': 'form-control'}),
#             'password': PasswordInput(attrs={'class': 'form-control'}) ,
#         }
#
#         labels = {
#             'username': "votre nom",
#             'password': 'votre mot de pass',
#             'email' : 'votre email',
#         }


class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
