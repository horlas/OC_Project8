from . import views
from django.urls import path
from django.conf.urls import url

app_name = "quality"

urlpatterns = [
    path('login/' , views.login , name='login') ,


]
