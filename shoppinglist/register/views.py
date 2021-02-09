from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate 
from django.contrib.auth import login 
from nouser.views import login_nouser
from django.contrib import messages
from main.decorators import unauthenticated_user
from main.models import UserProfile  

from django.contrib.auth.views import LoginView


@unauthenticated_user 
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



