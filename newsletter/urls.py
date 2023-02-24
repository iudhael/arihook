from django.urls import re_path
from newsletter import views
from django.contrib.auth import views as auth_views

app_name = 'newsletter'

urlpatterns = [

    re_path(r'^newsletter/subscribe', views.subscribepage, name='subscribe-letter'),
    re_path(r'^newsletter/mail_letter/$', views.mail_letter, name='mail-letter'),
    re_path(r'^newsletter/unsubscribe/$', views.unsubscribepage, name='unsubscribe-letter'),
    re_path(r'^newsletter/validation-unsubscribe/$', views.ValidationUnsubscribe, name='validation-unsubscribe'),


]



