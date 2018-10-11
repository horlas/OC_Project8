from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    '''form to log an user using the django User model, this form is passed to the login view'''

    class Meta:
        model = User
        fields = ['username', 'password']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    '''form to create an user using the Django User model, this form is passed to the signup view.
    PopRequestMixin from bootstrap_modal_forms.mixins : pops request out of the kwargs and attaches it to the form's
    instance.
    CreateUpdateAjaxMixin : Mixin which passes or saves object based on request type.
    '''
    class Meta:
        model = User
        fields = ['username', 'email']
