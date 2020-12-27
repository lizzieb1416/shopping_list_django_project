from django.urls import path


from . import views

app_name = "nouser"
urlpatterns = [
    path("home/", views.nouserhome, name="nouserhome"),
    path("", views.nouserhome, name="nouserhome"),
    path("home/create_newlist_nouser", views.nouser_create_slist, name="create_newlist_nouser"),
    path("home/<int:id>", views.nouser_new_list, name="nouser_newlist"),
    path("home/login_no_user/<int:id>", views.login_nouser, name="login_no_user"),
    path("home/register_nouser/<int:id>/", views.register_nouser, name="register_nouser"),
]
