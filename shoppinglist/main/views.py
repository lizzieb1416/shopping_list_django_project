from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import SList, Item
from django.db.models import Sum, Count
from .forms import CreateNewList
from django.contrib import messages
    

def list_renderer(response, id):
    sl = SList.objects.get(id=id)
    
    
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

                
            return HttpResponseRedirect("/%i" %sl.id)
        
        else:
            total = sl.item_set.aggregate(total_price=Sum("price"), total_items=Count('name'))
            print(total)
            
            return render(response, "main/list_renderer.html", {"sl":sl})


def userhome(response):
    # username = response.user.get_username()
    sl = response.user.slist.all()
    print(sl)
 
    if response.method == "POST":
        print(response.POST)
        
        if response.POST.get("delete_sl"):
            for s in sl:
                if response.POST.get("c" + str(s.id)) == "clicked":
                    s.delete()
                    print("{} deleted".format(s))
               
        elif response.POST.get("create_sl"):
            n = response.POST.get("input_sl")
            s = SList(name=n)
            s.save()
            response.user.slist.add(s)
            
            return HttpResponseRedirect("/%i" %s.id)
        
        return HttpResponseRedirect("/userhome")
    
    else:           
        return render(response, "main/userhome.html")
    

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
    











# def createlist(response):
#     if response.method == "POST":
#         form = CreateNewList(response.POST)
        
#         if form.is_valid():
#             n = form.cleaned_data["name"]
#             s = SList(name=n)
#             s.save()
#             response.user.slist.add(s)
    
#         return HttpResponseRedirect("/%i" %s.id)
    
#     else:
#         form = CreateNewList()
#     return render(response, "main/createlist.html", {"form":form})