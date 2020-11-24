from django.urls import path


from . import views

urlpatterns = [
    path("home/", views.nouserhome, name="nouserhome"),
    path("", views.nouserhome, name="nouserhome"),
      
]
