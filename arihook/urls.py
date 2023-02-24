"""arihook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from authentification import views
from django.contrib.sitemaps.views import sitemap


from arihook.sitemaps import *

sitemaps = {
    'modeles': ModeleSitemap,
    'image_detail' : Image_detailSitemap,

}

urlpatterns = [

    re_path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    re_path('', include('catalogue.urls', namespace='catalogue')),
    re_path('', include('authentification.urls', namespace='authentification')),
    re_path('', include('newsletter.urls', namespace='newsletter')),
    re_path(r'^$', views.main, name="home"),
    path('arihookadmin_panel_site/', admin.site.urls),


            # reinitialisation du mot de pass
    re_path(r'^authentification/password-reset/$', auth_views.PasswordResetView.as_view(
            template_name='authentification/password_reset.html'
        ),
            name="password_reset"),

        #  page  qui indique qu'un mail a été envoiyé pour  la reinitialisation
    re_path(r'^authentification/password-reset/done/$', auth_views.PasswordResetDoneView.as_view(
            template_name='authentification/password_reset_done.html'),
            name="password_reset_done"),

        # page de confirmation de reinitialisation
        #<uidb64>  id de l'utilisateur encoder en base 64
        # <token> --> pour la securisation verifie que le mot de pass est valide
    re_path(r'^authentification/password-reset-confirm/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$', auth_views.PasswordResetConfirmView.as_view(
            template_name='authentification/password_reset_confirm.html'),
            name="password_reset_confirm"),

    re_path(r'^authentification/password-reset-complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='authentification/password_reset_complete.html'), name="password_reset_complete"),

    
     

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


