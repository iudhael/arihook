from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str #force_text
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from catalogue.models import Categories

from arihook import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from catalogue.views import today_date
from . tokens import generateToken
from .forms import CreateUserform, ParagraphErrorList, UserUpdateForm, ResendConfirmationForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
import random





# Create your views here.
"""

def index(request, *args, **kwargs):
    return render(request, 'authentification/register.html')
"""


def main(request):
    categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date).order_by('nom_categorie')
    categorie_objs = list(categories)

    random.shuffle(categorie_objs)
    categorie_objs = categorie_objs[:3]

    # print(categorie_objs)
    navbar = "home"
    context = {
        'categorie_objs': categorie_objs,
        "navbar": navbar,
    }

    return render(request, 'catalogue/home.html', context)


@login_required(login_url='authentification:login')
def profileuser(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)

        # enregistrer si le formulaire est valide
        if user_form.is_valid():
            user_form.save()


            messages.success(request, 'Account has been updated!! ')

            return redirect('authentification/profile.html')

    else:
        user_form = UserUpdateForm(instance=request.user)


    navbar ="profile"
    context = {
        'user_form': user_form,
        'navbar' : navbar

    }

    return render(request, 'authentification/profile.html', context)

def send_email(username,email_user,request,user):
    messages.success(request, f'{username}, your account has been successfully created. We have sent you an email.\n You must comfirm in order to activate your account.')

    """
    # send email when account has been created successfully
    subject = "Welcome to AriHook"
    message = "Welcome " + nom + " " + prenom + "\n thank for chosing our website .\n To order login you need to comfirm your email account.\n thanks\n\n\n AriHook"

    from_email = settings.EMAIL_HOST_USER
    to_list = [email_user]
    send_mail(subject, message, from_email, to_list, fail_silently=False)
    """

    # send the confirmation email
    current_site = get_current_site(request)
    email_suject = "confirm your email AriHook Login!"
    messageConfirm = render_to_string("emailConfimation.html", {
        'name': username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generateToken.make_token(user)
    })

    email = EmailMessage(
        email_suject,
        messageConfirm,
        settings.EMAIL_HOST_USER,
        [email_user]
    )

    email.fail_silently = False
    email.send()
    """
    if email.send() :
        email_envoyer = True
    else:
        email_envoyer = False
    return email_envoyer
    """

def registerpage(request):

    # si la personne est autentifié
    if request.user.is_authenticated:
        return redirect('catalogue:home')
    else:
        form = CreateUserform()
        #form_valid = False
        if request.method == 'POST':
            form = CreateUserform(request.POST, error_class=ParagraphErrorList)

            if form.is_valid():

                user = form.save(commit=False)# avec commit on n'eregistre pas mais on stocke


                user.is_active = False
                user.save()

                
                #recuperation du username pour le message de confirmation
                username = form.cleaned_data.get('username')
                email_user = form.cleaned_data.get('email')
                #nom = form.cleaned_data.get('last_name')
                #prenom = form.cleaned_data.get('first_name')

                #send_email(nom, prenom, username, email_user, request, user)

                send_email(username, email_user, request, user)


                """
                renvoyer le mail de confirmation si le premier mail n'a pas ete envoyer
                email_envoyer = send_email(nom, prenom, username, email_user, request, user)
                if not email_envoyer:
                    return redirect('authentification:login')
                else:
                    btn_resend_email = request.POST.get('resend_email')
                    print(btn_resend_email)


                    context = {
                        'form': form,
                        'email_envoyer': email_envoyer,

                    }
                    return render(request, 'authentification/register.html', context)

                """
                """
                email_envoyer =True
                context = {
                    'form': form,
                    'email_envoyer': email_envoyer,

                }

                return render(request, 'authentification/register.html', context)
                """
                return redirect('catalogue:home')

    context = {
        'form':form,

        }
    return render(request, 'authentification/register.html', context)   
  


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('catalogue:home')
    else:
        if request.method == 'POST':
            #demander le nom et le passe
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')

            #print(username)
            #print(password)

            #verifier si l'utilisateur existe dans la bdd
            user = authenticate(request, username=username, password=password)
            if user is not None:
                my_user = User.objects.get(username=username)
                if my_user.is_active == False:
                        messages.error(request, 'You have not confirm your  email do it, in order to activate your account')
                        return redirect('login')

            #si il existe on le redirige a la page d'acceuil
            if user is not None:
                login(request, user)
                if remember_me:
                    messages.success(request, f'Hello  {request.user}')
                    response = redirect('catalogue:home')
                    response.set_cookie('username', username, max_age=3600 * 24 * 30)  # 1 mois
                    response.set_cookie('password', password, max_age=3600 * 24 * 30)
                    request.session.set_expiry(86400*30)
                    return response
                else:
                    messages.success(request, f'Hello  {request.user}')
                    request.session.set_expiry(86400)
                    return redirect('home')
                #username = user.username

            else:
                #dans le cas ou l'utilisateur n'existe pas ou a mal taper ses identifiants un message est envoyé
                messages.info(request, 'Username OR Password is incorrect')



    context = {
       
        }
    return render(request, 'authentification/login.html', context)    

def logoutuser(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    #return redirect('catalogue:home')
    response = HttpResponseRedirect(request.META['HTTP_REFERER'])
    response.delete_cookie('username')
    response.delete_cookie('password')

    return response




def resend_confirmation(request):
    if request.method == 'POST':
        form = ResendConfirmationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).last()
            #print(user.username)
            if user:
                if user.is_active == False:
                    current_site = get_current_site(request)
                    subject = 'Activer votre compte'
                    message = render_to_string('emailConfimation.html', {
                        'name': user.username,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': generateToken.make_token(user)
                    })
                    email = EmailMessage(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email]

                    )
                    email.fail_silently = False
                    email.send()
                    messages.success(request, "Mail envoyer avec succes !")
                    return redirect('authentification:login')
                else:
                    messages.error(request, "Ce compte à déjà été activé !")
                    return redirect('authentification:login')
            else:
                messages.error(request,"Ce mail n'a pas été retrouvé !")
                return redirect('authentification:register')
    else:
        form = ResendConfirmationForm()

    context = {'form': form}

    return render(request, 'authentification/resend_confirmation.html', context)



















def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generateToken.check_token(user, token):
        user.is_active  = True        
        user.save()
        messages.success(request, "You are account is activated you can login by filling the form below.")
        return redirect("authentification:login")
    else:
        messages.success(request, 'Activation failed please try again')
        return redirect('catalogue:home')
