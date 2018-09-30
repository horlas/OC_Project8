from . import views
from django.urls import path


app_name = "quality"

urlpatterns = [
    path('', views.index, name='index'),
    path('query_data/', views.get_query, name='query_data'),


    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name = 'logout'),
    path('success_signup/' , views.SuccessSignup.as_view() , name='success_signup') ,
    path('home/', views.HomeView.as_view(), name='home'),


]
