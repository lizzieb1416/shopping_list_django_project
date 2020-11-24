from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("<int:id>", views.list_renderer, name="list_renderer"),
    path("createlist/", views.createlist, name="createlist"),
    path("userhome/", views.userhome, name="userhome"),
    path("<int:id>/sortlist/", views.sort_list, name="sortlist"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)