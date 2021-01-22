from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import SList, Item, UserProfile, Friend
from django.db.models import Sum, Count
from .forms import CreateNewList
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def list_renderer(response, id):
    sl = SList.objects.get(id=id)
    #sl = response.user.userprofile.slist.get(id=id)
    # list_owner = Friend.objects.get(current_user=response.user)
    # friends = list_owner.users.all()
    
    friends = response.user.friends.get().users.all()
        
    if sl in response.user.slist.all():
    
        if response.method == "POST":
            print("posting: {}".format(response.POST))
            
            if response.POST.get("deleteItem"):
                sl.delete_item_from_response_post(response.POST)
            
            elif response.POST.get("addItem"):
                try:
                    sl.add_item_from_response_post(response.POST)
                except ValueError as my_value_error:
                    messages.add_message(response, messages.ERROR, my_value_error)
            
            elif response.POST.get("sortList"):
                sort_list(response, sl.id)
                return HttpResponseRedirect("/%i/sortlist" %sl.id)
            
            elif response.POST.get("delete_list"):
                SList.delete_slist(response.POST)
                return redirect("/userhome")
            
            elif response.POST.get("share_list"):
                
                username_friend = response.POST.get("friend_to_share")
                friend = User.objects.get(username=username_friend)
                
                sl.user.add(friend)            
                
            return HttpResponseRedirect("/%i" %sl.id)
        
        else:
            total = sl.item_set.aggregate(total_price=Sum("price"), total_items=Count('name'))
            print(total)
            
            return render(response, "main/list_renderer.html", {"sl":sl, "friends":friends})

    else:
        return HttpResponse("OOPS! YOU DON'T HAVE ACCES TO THIS PAGE")


@login_required(login_url='login')
def userhome(response): 
    # username = response.user.get_username()
    sl = response.user.slist.all()
    print(sl)
 
    if response.method == "POST":
        print(response.POST)
                    
        if response.POST.get("delete_list"):
            sl_id = int(response.POST["delete_list"])
            sl = SList.objects.get(id=sl_id)
            sl.delete() 
                        
        elif response.POST.get("create_sl"):
            n = response.POST.get("input_sl")
            s = SList(name=n)
            s.save()
            response.user.slist.add(s)
        
        return HttpResponseRedirect("/userhome")
    
    else:           
        return render(response, "main/userhome.html") 
    
    
@login_required(login_url='login')
def sort_list(response, id):
    sl = SList.objects.get(id=id)
    item_type_list = list(set([myitem.item_type for myitem in sl.item_set.all()]))
    items_data = {}
        
    i = 0
    
    while i < len(item_type_list):
        
        total_price = []
        for item in sl.item_set.all(): 
            
            if sl.item_set.filter(item_type=item_type_list[i]):
                total_price.append(item.obtaine_tot_price_per_item)
                items_data[item_type_list[i]] = (sl.item_set.filter(item_type=item_type_list[i]), sum(total_price)) 
                print("total AFTER: {}".format(total_price))
                print(items_data)
            
            total_price.clear()
            print("cleared")
        i += 1
        

    print(items_data)
        
    return render(response, "main/sortlist.html", {"sl":sl, 
                                                   "items_data":items_data,
                                                   })
    
    











