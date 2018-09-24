from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError

from django.http import HttpResponseRedirect

# from  .models import User
from .forms import CustomAuthenticationForm, CustomUserCreationForm

from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import LoginAjaxMixin, PassRequestMixin


from django.views.generic import TemplateView


def index(request):
   
    return render(request, 'quality/index.html')

def test(request):

    return render(request, 'quality/test.html')

# def home(request):
#     return render(request, 'quality/home.html')


class CustomLoginView(LoginAjaxMixin, SuccessMessageMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'quality/registration/login.html'
    success_message = 'Vous etes à présent connecté'
    redirect_field_name = 'test'

    def get_success_url(self):
        return reverse_lazy('quality:home')
    # success_url = reverse_lazy('quality:test')


class SignUpView(PassRequestMixin, SuccessMessageMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'quality/registration/signup.html'
    success_message = 'Creation de compte réussi. Vous pouvez vous connectez.'
    # success_url = reverse_lazy('index')
    def get_success_url(self):
        return reverse_lazy('quality:test')

class HomeView(TemplateView):
    template_name = "quality/home.html"







# def user_signup(request):
#     # if this is a POST request we need to process the form data
#     response_data = {}
#     if request.method == 'POST' and request.is_ajax:
#         username = request.POST['username'].lower()
#         email = request.POST['email']
#         password = request.POST['password']
#
#         new_user = User.objects.create(
#             username=username ,
#             email=email ,
#             )
#
#         #Sets the user’s password to the given raw string, taking care of the password hashing
#         new_user.set_password(password)
#         new_user.save()
#
#         #Use authenticate() to verify a set of credentials.
#         log_user = authenticate(username=userusername , password=password)
#         if log_user is not None:
#
#             #An authenticated user attached to the current session - this is done with a login() function.
#             login(request , log_user)
#             response_data = {'message': 'Votre compte est bien créé. Vous etes connecté'}
#         else:
#             response_data = {'message': 'Echec à la création du compte'}
#
#         return JsonResponse(response_data)

    #     # create a form instance and populate it with data from the request:
    #     form = UserForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         email = form.cleaned_data['email']
    #         password = form.cleaned_data['password']
    #
    #         user = User.objects.filter(email=email)
    #         if not user.exists():
    #             # If a contact is not registered, create a new one.
    #             user = User.objects.create(
    #                 username = username,
    #                 email = email,
    #                 password = password
    #             )
    #
    #
    #
    #
    #
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         return render(request,'quality/thanks.html')
    #
    # # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = UserForm()
    #
    # return render(request, 'quality/login.html', {'form': form})

