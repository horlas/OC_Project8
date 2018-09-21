from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError

from django.http import HttpResponseRedirect
from .forms import UserForm
from  .models import User

def index(request):
   
    return render(request, 'quality/index.html')


def user_signup(request):
    # if this is a POST request we need to process the form data
    response_data = {}
    if request.method == 'POST' and request.is_ajax
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.filter(email=email)
            if not user.exists():
                # If a contact is not registered, create a new one.
                user = User.objects.create(
                    username = username,
                    email = email,
                    password = password
                )





            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request,'quality/thanks.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, 'quality/login.html', {'form': form})

