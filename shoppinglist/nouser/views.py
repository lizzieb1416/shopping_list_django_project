from django.shortcuts import render
from main.models import SList, Item
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Sum, Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def nouserhome(response):
    
    return render(response, "nouser/nouserhome.html", {})

def nouser_create_slist(response):
    
    if response.method == "POST":
        if response.POST.get("create_sl"):
            sl_name = response.POST.get("input_sl")
            tmp_sl = SList(name=sl_name) 
            tmp_sl.save() 
            print(response.user)
            return HttpResponseRedirect("/home/%i" %tmp_sl.id)
            
    return render(response, "nouser/nouser_create_slist.html", {})

def nouser_new_list(response, id):
    
    sl = SList.objects.get(id=id)
    
    if response.method == "POST":
        print("posting: {}".format(response.POST))
        
        if response.POST.get("deleteItem"):
            sl.delete_item_from_response_post(response.POST)
        
        elif response.POST.get("addItem"):
            try:
                sl.add_item_from_response_post(response.POST)
            except ValueError as my_value_error:
                messages.add_message(response, messages.ERROR, my_value_error)
                
        elif response.POST.get("saveList"):
            return HttpResponseRedirect("/home/login_no_user/%i" %sl.id)
                    
        return HttpResponseRedirect("/home/%i" %sl.id)
    
    else:
        total = sl.item_set.aggregate(total_price=Sum("price"), total_items=Count('name'))
        print(total)
        
        return render(response, "nouser/nouser_newlist.html", {"sl":sl})
    
    
def login_nouser(response, id):
    
    sl = SList.objects.get(id=id)
    
    if response.method == "POST":
        if response.POST.get("submit"):
            username = response.POST.get('username')
            password = response.POST.get('password')
            user = authenticate(response, username=username, password=password)
            login(response, user)
            print(user)
            
            if user is not None:
                login(response, user)
                print("logged in!!!")
                
                user.slist.add(sl)
                return HttpResponseRedirect("/userhome")  
        
        elif response.POST.get("create_account"):
            return HttpResponseRedirect("/home/register_nouser/%i" %sl.id)
            
    else:
        return render(response, "nouser/login_nouser.html")
        

def register_nouser(response, id):
    
    sl = SList.objects.get(id=id)
    
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1']
                        )
            login(response, new_user)
            new_user.slist.add(sl)
            return HttpResponseRedirect("/userhome")
    else:
        form = UserCreationForm()
    
    return render(response, "nouser/register_nouser.html", {"form":form, "id":sl.id})
        
        


