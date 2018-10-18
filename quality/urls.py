from . import views
from django.urls import path


app_name = "quality"

urlpatterns = [

    path('', views.accueil, name='accueil'),


    # connected views
    path('my_account/', views.myaccount, name='myaccount'),
    path('food/', views.food, name='food'),

    # unconnected views
    path('query_data/', views.query_data, name='query_data'),
    path('sub_product/', views.sub_product, name= 'sub_product'),
    path('user_choice/', views.user_choice, name='user_choice'),
    path('credits/', views.credits, name='credits'),

    # authentification view
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('success_signup/', views.SuccessSignup.as_view() , name='success_signup'),
]
