from django.urls import path
from . import views

app_name = "accounts" 
urlpatterns = [
    path("profile/details", views.profile_details, name="profile_details"),
    path("profile/friends/", views.friends, name="friends"),
    path("profile/friends/<int:id>", views.profile_details, name="profile_details_by_id"),
    path("profile/friends/<str:action>/<int:id>", views.add_delete_friends, name="add_delete_friends"),
    path("profile/edit_profile/", views.edit_profile, name="edit_profile"),
    path("profile/change_password", views.change_password, name="change_password"),
]


