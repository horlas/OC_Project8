# Create your views here.
from django.shortcuts import render, get_object_or_404
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import LoginAjaxMixin, PassRequestMixin
from django.http import JsonResponse
from .methods import query_off, best_substitute
from .models import SelectedProduct, SubstitutProduct, Backup
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_ajax.decorators import ajax



from django.views.generic import TemplateView


def accueil(request):
   
    return render(request, 'quality/index.html')

@login_required
def myaccount(request):
    return render(request, 'quality/account.html')



@login_required
def food(request):
    #define the connected user
    user = request.user

    backup_list = Backup.objects.filter(user_id = user.id)

    #requete inner join sur selectedproduct/Backup/substituProduct
    #p_list = SelectedProduct.objects.filter(backup__user_id= user.id , substitutproduct__selected_product_id=18)
    sel_product_list = SelectedProduct.objects.filter(backup__user_id=user.id , substitutproduct__user_id=user.id)
    sub_product_list = SubstitutProduct.objects.filter(user_id = user.id)
    # Slice pages
    paginator0 = Paginator(sel_product_list, 1)
    paginator1 = Paginator(sub_product_list, 1)
    #Get current page
    page = request.GET.get('page')
    try:
        #return only the first product and not the others
        sel_products = paginator0.get_page(page)
        sub_products = paginator1.get_page(page)
        print("YOOOOO", sub_products)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        sel_products = paginator0.page(1)
        sub_products = paginator1.page(1)
    except EmptyPage:
        #If page out of range (e.g 99999), deliver last page of results.
        sel_products = paginator0.page(paginator0.num_pages)
        sub_products = paginator1.page(paginator1.num_pages)
    context = {
        'sel_products' : sel_products,
        'sub_products': sub_products
    }

    return render(request, 'quality/food.html', context)


def query_data(request):
    query = request.GET.get('query', None)
    print(query)

    if not query:
        title = "saisissez un produit ! "
        context = {'title': title }
        return render(request, 'quality/index.html', context)
    else:
        #query_off function calls OFF API and return 6 products
        data = query_off(query)
        title = 'Votre recherche est :  "{}"'. format(query)
        context = {
            'title': title,
            'data' : data
        }

    return render(request, 'quality/query_data.html', context)

def sub_product(request):
    # get the user choice from the checkbox
    choices = request.GET.get('subscribe', None)

    #split the checkbox's return in order to make a python list
    choices = choices.split(', ')

    #record selected product in session
    record_session = ['selected_name', 'selected_category', 'selected_img', 'selected_nutriscore', 'selected_url']
    for value , choice in zip(record_session , choices):
        request.session[value] = choice

    cat = request.session['selected_category']


    #request to OpenFoodFact and return six best products with the same category
    data = best_substitute(cat)
    title = 'six produits meilleurs ont été trouvés dans la catégorie {}'.format(cat)
    context = {
        'title': title ,
        'data': data
    }
    return render(request, 'quality/sub_product.html', context)

def user_choice(request):
    # get the user choice from the checkbox
    choices = request.GET.get('subscribe' , None)

    # split the checkbox's return in order to make a python list
    choices = choices.split(', ')

    #record selected product in database
    p_selected = SelectedProduct.objects.create(
        name = request.session['selected_name'],
        url = request.session['selected_url'],
        img = request.session['selected_img'],
        n_grade = request.session['selected_nutriscore'],
        category = request.session['selected_category'])

    #record the backup with selected_product_id and user_id
    backup = Backup.objects.create(
        user_id = request.user,
        selected_product_id = p_selected
    )

    #record the substitute product with all the foreign key
    p_substitut = SubstitutProduct.objects.create(
        name = choices[0],
        category = choices[1],
        img = choices[2],
        n_grade = choices[3],
        url = choices[4],

        backup_id = backup,
        user_id = request.user,
        selected_product_id = p_selected
    )


    #record selected product in session
    record_session = ['substitut_name', 'substitut_category', 'substitut_img', 'substitut_nutriscore', 'substitut_url']
    for value , choice in zip(record_session , choices):
        request.session[value] = choice
    return render(request, 'quality/user_choice.html')




# Authentication views


class CustomLoginView(LoginAjaxMixin, SuccessMessageMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'quality/registration/login.html'
    success_message = 'Vous etes à présent connecté'



    #
    # def get_success_url(self):
    #     return reverse_lazy('quality:accueil')

    # def get_success_url(self):
    #     url = "{}".format(self.request.META.get('HTTP_REFERER'))
    #     return reverse_lazy(url)

    # def post(self, request, *args, **kwargs):
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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

class LogSignView(CustomLoginView,CustomAuthenticationForm):

    form_class1 = CustomAuthenticationForm
    # form_class2 = CustomUserCreationForm
    template_name = 'quality/registration/login_signin.html'

    #
    # def get_success_url(self):
    #     return reverse_lazy('quality:accueil')



class SuccessSignup(SignUpView):
    template_name = 'quality/registration/success_signup.html'

    def get_context_data(self , **kwargs):
        context = super(SignUpView , self).get_context_data(**kwargs)
        return context


class HomeView(TemplateView):
    template_name = "quality/home.html"


class LogoutView(TemplateView):
    template_name = 'quality/index.html'
    title = "Vous etes déconnecté"

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)




