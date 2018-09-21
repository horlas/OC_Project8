from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from .models import User

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {

            'username': TextInput(attrs={'class': 'form-control'}) ,
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}) ,
        }

        labels = {
            'username': "votre nom",
            'password': 'votre mot de pass',
            'email' : 'votre email',
        }



