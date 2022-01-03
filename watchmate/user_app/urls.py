from rest_framework.authtoken.views import obtain_auth_token
from user_app.views import register,logout
from django.urls import path

urlpatterns =[
    path('login/',obtain_auth_token,name='login'),
    path('register/',register,name='register'),
    path('logout/',logout,name='logout'),
]
