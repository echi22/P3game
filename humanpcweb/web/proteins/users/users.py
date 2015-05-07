# -*- coding: utf-8 -*-
from web.proteins.models import list_to_json
from web.proteins.models import Score
from django.http import HttpResponse
from web.proteins.models import UserProfile
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from datetime import datetime
import random
from random import Random
from django.shortcuts import render_to_response
from time import time
from web.proteins.models import UserProfile
from django import forms
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib import messages
class GetLevel(forms.Form):
  level = forms.IntegerField()

class RegisterForm(forms.Form):
  username = forms.CharField(max_length=50)
  password = forms.CharField(max_length=50)
  password2= forms.CharField(max_length=50)
  email=forms.EmailField()
  birthday = forms.DateField()
  knows_proteins = forms.BooleanField(initial=False, required=False) 
  game_is_beta = forms.BooleanField(initial=False,required=False)
def create(request,username,email,password,first_name,anonymous,birthday,knows_proteins):
    user = User.objects.create_user(username,email,password)
    user.first_name=first_name
    user.save()
    profile=UserProfile(user=user,anonymous=anonymous,game=0,level=0,points=0,user_level=1,best_score_in_level=0,birthday=birthday,knows_proteins=knows_proteins)
    profile.save()
    Score.for_user(user, 0, 0).save()
    user = authenticate(username=username, password=password)
    auth.login(request, user)
def register(request):
    form=RegisterForm(request.POST)
    if(form.is_valid()):
        c=form.cleaned_data
        if(c['game_is_beta']):
            if not(User.objects.filter(username=c['username']).exists()):
                if(c['password'] == c['password2']):
                    
                    create(request,c['username'],c['email'],c['password'],'',False,c['birthday'],c['knows_proteins'])
                    return HttpResponseRedirect('/')
                else:
                    messages.error(request,'Las contraseñas no coinciden',extra_tags='register')
            else:
                messages.error(request,'Ya existe un usuario con ese nombre',extra_tags='register')
        else:
            messages.error(request,'Tenés que indicar que entendés que el juego está en desarrollo',extra_tags='register')
    else:
        messages.error(request,'El mail o la fecha de nacimiento es inválida',extra_tags='register')
    c = form    
    data = {"username" : c["username"],"pass":c["password"],"pass2":c["password2"],"birthday":c["birthday"],"email":c["email"],"knows_proteins":c["knows_proteins"],"beta":c["game_is_beta"]}
    return render_to_response('site/index.html',data, context_instance=RequestContext(request))


# def create_user(request):
#     if(request.method == 'POST'):
#         username=request.POST["username"]
#         password=request.POST["password"]
#         password2=request.POST["password2"]
#         email=request.POST["email"]
#         first_name=request.POST["first_name"]
#         if(password == password2):
#             create(request,username,email,password,first_name,False)
#             saved={'saved':True,'error':False}
#             return render_to_response('protein/create_user.html',saved, context_instance=RequestContext(request))
#         else:
#             saved={'saved':True,'error':True}
#             return render_to_response('protein/create_user.html',saved, context_instance=RequestContext(request))
#     else:
#         return render_to_response('protein/create_user.html', context_instance=RequestContext(request))

      
def create_anonymous_user(request):
    create(request,'anonymous'+str(datetime.today()),"","","",True)
    print  " session key before:"+request.session.session_key
    #print  "create anonymous user name "+user.first_name+ " authenticated "+str (user.is_authenticated())
    print  " session key after: "+request.session.session_key
#    request.session.modified = True
    return HttpResponse()
    

class LoginForm(forms.Form):
  username = forms.CharField(max_length=50)
  password = forms.CharField(max_length=50)


def login_user(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        try:
          type = request.POST['type']
        except KeyError:
          type= ""
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if(type=='ajax'):
                    result='{"result":"Bienvenido '+username+'","failed":false}'
                    return HttpResponse(result, mimetype='application/json')
                else:
                    logged={'attempted':True,'error':False,'username':username}
                    return render_to_response('protein/login_user.html',logged, context_instance=RequestContext(request))
            else:
                if(type=='ajax'):
                    result='{"result":"Usuario o contraseña incorrectos.","failed":true}'
                    return HttpResponse(result, mimetype='application/json')
                else:
                    logged={'attempted':True,'error':True}
                    return render_to_response('protein/login_user.html',logged, context_instance=RequestContext(request))
        else:
            if(type=='ajax'):
                    result='{"result":"Usuario o contraseña incorrectos","failed":true}'
                    return HttpResponse(result, mimetype='application/json')
            else:
                logged={'logged':True,'error':True}
                return render_to_response('protein/login_user.html',logged, context_instance=RequestContext(request))
    else:
         return render_to_response('protein/login_user.html', context_instance=RequestContext(request))
def login(request):
    form=LoginForm(request.POST)
    
    if( form.is_valid()):
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
    messages.error(request,'Usuario o contraseña incorrectos',extra_tags='login')
    return HttpResponseRedirect('/users/login_or_register')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
def login_or_register(request):
    if(request.user.is_anonymous()):
        return render_to_response('site/index.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')



def register_anonymous(request):
    if(request.method == 'POST'):
        type=request.POST["type"]
        if(request.POST["password"] == request.POST["password2"]):
            modify(request.user,request.POST["username"],request.POST["password"],request.POST["email"],request.POST["first_name"])
            profile=request.user.get_profile()
            profile.anonymous=False
            profile.save()
            if(type=='ajax'):
                    result='{"result":"The user has been created sucesfully.","failed":false}'
                    return HttpResponse(result, mimetype='application/json')
            else:
                saved={'saved':True,'error':False}
                return render_to_response('protein/create_user.html',saved, context_instance=RequestContext(request))
        else:
            if(type=='ajax'):
                    result=u'{"result":"Las contraseñas no coinciden","failed":true}'
                    return HttpResponse(result, mimetype='application/json')
            else:
                saved={'saved':True,'error':True}
                return render_to_response('protein/create_user.html',saved, context_instance=RequestContext(request))
    else:
        return render_to_response('protein/create_user.html', context_instance=RequestContext(request))
    
def get_user(request):
    user=request.user
    print  " get_user session key :"+request.session.session_key
    if user.is_authenticated():
        profile_json=user.get_profile().json()
        result='{"username": "%s", "email":"%s", "first_name": "%s", "last_name": "%s", "profile": %s}' % (user.username,user.email,user.first_name,user.last_name,profile_json)
    else:
        result='{"username":""}'
    return HttpResponse(result, mimetype='application/json')
def modify(user,username,password,email,first_name):
    user.username=username
    user.set_password(password)
    user.email=email
    user.first_name=first_name
    user.save()
