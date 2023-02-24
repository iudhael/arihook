from django.urls import re_path
from authentification import views
from django.contrib.auth import views as auth_views


app_name = 'authentification'

urlpatterns = [
   
    #url(r'^authentification', views.index, name="authentification"),

    re_path(r'^authentification/resend-confirmation-email/', views.resend_confirmation, name='resend-confirmation-email'),
    re_path(r'^authentification/register/', views.registerpage, name='register'),
    re_path(r'^authentification/login/', views.loginpage, name='login'),
    re_path(r'^activate/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$', views.activate, name='activate'),
    re_path(r'^authentification/logout/', views.logoutuser, name='logout'),
    re_path(r'^authentification/profile/', views.profileuser, name="profile"),


    
]



