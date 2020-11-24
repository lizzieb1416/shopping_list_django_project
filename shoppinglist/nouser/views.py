from django.shortcuts import render

# Create your views here.

def nouserhome(response):
    
    return render(response, "nouser/nouserhome.html", {})

