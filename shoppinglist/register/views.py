from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from nouser.views import login_nouser
from django.contrib import messages
from main.decorators import unauthenticated_user
from main.models import UserProfile



@unauthenticated_user # TODO look for the way to apply this to the login page too
def register(response):    
    
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            # User autentification
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1']
                                    )
            login(response, new_user)
                                     
            # Welcome message
            user = form.cleaned_data.get('username')
            messages.success(response, 'Hello ' + user + ', your account was succesflly created!')
            
            return redirect("/userhome")
            
                
    else:
        form = RegisterForm()
        
    return render(response, "register/register.html", {"form":form})


# TODO make a login page, I dont like the login page by default from Django 
# def loginPage(response):
    
#     if response.method == 'POST':
#         username = response.POST.get('username')
#         password = response.POST.get('password')
        
#         user = authenticate(response, username=username, password=password)
        
#         if user is not None:
#             login(response, user)
#             return redirect("/userhome")
#         else:
#             return render(response, 'registration/login.html',{})
    
#     return render(response, 'registration/login.html', {})