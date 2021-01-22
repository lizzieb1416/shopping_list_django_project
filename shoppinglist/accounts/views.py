from django.shortcuts import render
from main.models import SList, Item, UserProfile, Friend
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserChangeForm
from . forms import EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


@login_required(login_url='login')
def profile_details(response, id=None):
    
    if id:
        user = User.objects.get(id=id)
    else:
        user = response.user
    
    args = {'user':user}
    return render(response, "accounts/profile_details.html", args)


@login_required(login_url='login')    
def friends(response):
    
    users = User.objects.exclude(id=response.user.id)
        
    friends = response.user.friends.get().users.all()
    
    args = {'users':users, 'friends':friends}
    return render(response, "accounts/friends.html", args)


@login_required(login_url='login')   
def add_delete_friends(response, action, id):
    new_friend = User.objects.get(id=id)
    if action == 'add':
        Friend.make_friend(response.user, new_friend)
    elif action =='delete':
        Friend.delete_friend(response.user, new_friend)
    return redirect('accounts:friends')


@login_required(login_url='login') 
def edit_profile(response):
    
    if response.method == 'POST':
        form = EditProfileForm(response.POST, instance=response.user)
        
        if form.is_valid():
            form.save()
            messages.success(response, 'Profile details succesfully updated !')
            return redirect('/profile/details')
    else:
        form = EditProfileForm(instance=response.user)
        args = {'form':form}
        return render(response, "accounts/edit_profile.html", args)
        
    # return render(response, "accounts/edit_profile.html", args)


@login_required(login_url='login') 
def change_password(response):
    
    if response.method == 'POST':
        form = PasswordChangeForm(data=response.POST, user=response.user)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(response, form.user)
            messages.success(response, 'Password succesfully updated !')
            return redirect('/profile/details')
        else:
            messages.error(response, 'Something went wrong. Try again.')
            return redirect("/profile/change_password")
    
    else:
        form = PasswordChangeForm(user=response.user)
        args = {'form':form}
        return render(response, "accounts/change_password.html", args)
