# Create your views here.
from django.shortcuts import render, get_object_or_404
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import LoginAjaxMixin, PassRequestMixin
from django.http import JsonResponse
from .methods import query_off
from django_ajax.decorators import ajax



from django.views.generic import TemplateView


def accueil(request):
   
    return render(request, 'quality/accueil.html')


def query_data(request):
    query = request.GET.get('query', None)
    print(query)

    if not query:
        title = "saisissez un produit ! "
        context = {'title': title }
        return render(request, 'quality/accueil.html', context)
    else:
        data = query_off(query)
        title = 'Votre recherche :  "{}"'. format(query)
        context = {
            'title': title,
            'data' : data
        }

    return render(request, 'quality/query_data.html', context)

class CustomLoginView(LoginAjaxMixin, SuccessMessageMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'quality/registration/login.html'
    success_message = 'Vous etes à présent connecté'

    def get_success_url(self):
        return reverse_lazy('quality:home')


class SignUpView(PassRequestMixin, SuccessMessageMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'quality/registration/signup.html'
    success_message = 'Création de compte réussie !'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


    def get_success_url(self):
        return reverse_lazy('quality:success_signup')


class SuccessSignup(SignUpView):

    template_name = 'quality/registration/success_signup.html'

    def get_context_data(self , **kwargs):
        context = super(SignUpView , self).get_context_data(**kwargs)
        return context


class HomeView(TemplateView):
    template_name = "quality/home.html"


class LogoutView(TemplateView):
    template_name = 'quality/accueil.html'
    title = "Vous etes déconnecté"

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)




