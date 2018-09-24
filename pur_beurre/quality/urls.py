from . import views
from django.urls import path
from django.conf.urls import url
from django.views.generic.base import TemplateView

app_name = "quality"

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('test/', views.test, name='test'),

]
