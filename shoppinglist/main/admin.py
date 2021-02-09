from django.contrib import admin
from .models import SList, Item, UserProfile, Friend

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(SList)
admin.site.register(Item)
admin.site.register(Friend)
