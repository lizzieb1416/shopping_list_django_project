from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from nouser.views import login_nouser

# Create your views here.

def register(response):
    
    
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1']
                                    )
            login(response, new_user)
            return redirect("/userhome")
            
                
    else:
        form = RegisterForm()
        
    return render(response, "register/register.html", {"form":form})

