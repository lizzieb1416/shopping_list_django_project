from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from copy import deepcopy
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', null=True, on_delete=models.CASCADE)
    # name = models.CharField(max_length=200, null=True)
    # last_name = models.CharField(max_length=200, null=True)
    # email = models.CharField(max_length=200, null=True)
    # date_created = models.DateTimeField(auto_created=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    
def create_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])
    
post_save.connect(create_profile, sender=User)
    

class SList(models.Model):
    #profile = models.ManyToManyField(UserProfile, related_name="slist", null=True, blank=True)
    user = models.ManyToManyField(User, related_name="slist", null=True, blank=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    def delete_item_from_response_post(self, response_post):
        for item in self.item_set.all():
            if response_post.get("c" + str(item.id)) == "clicked":
                item.delete()        
    
    
    def add_item_from_response_post(self, response_post):
        name = response_post.get("name")
        item_type = response_post.get("item_type")
        
        
        if self.item_set.filter(name=name, item_type=item_type):
            item_to_delete = self.item_set.get(name=name, item_type=item_type)
            item_to_delete.delete()
        
        slist = self            
        name = response_post.get("name")
        quantity = response_post.get("quantity")
        unit = response_post.get("unit")
        item_type = response_post.get("item_type")
        price = response_post.get("price")
        complete = False 
        
        item_created = Item.create(slist, name=name, quantity=quantity, unit=unit, item_type=item_type, price=price, complete=complete)
        item_created.save()            
      
    def total_sl_price(self):
        total_price = []
        for item in self.item_set.all():
            total_price.append(item.obtaine_tot_price_per_item)
        
        return sum(total_price)
    
    def total_items_in_list(self):
        total_items = []
        for item in self.item_set.all():
            total_items.append(item.quantity)
        
        return sum(total_items)

    def duplicate(self):
        '''Duplicate a model instance, making copies of all foreign keys pointing to it.'''
        
        foreign_keys_to_copy = list(self.item_set.all())
        print(foreign_keys_to_copy)
        sl_copy = deepcopy(self)
        sl_copy.pk = None
        sl_copy.save()
        
        # self.pk = None
        # self.save()
        
        foreign_keys = {}
        
        for fk in foreign_keys_to_copy:
            fk.pk = None
            
            try:
                foreign_keys[fk.__class__].append(fk)
            except KeyError:
                foreign_keys[fk.__class__] = [fk]
                
        for cls, list_of_fk in foreign_keys.items():
            
            cls.objects.bulk_create(list_of_fk)
         

        print(foreign_keys)


class Item(models.Model):
    slist = models.ForeignKey(SList, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    quantity = models.IntegerField(blank=True)
    unit = models.CharField(max_length=100, blank=True)
    item_type = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=30, decimal_places=2, blank=True)
    complete = models.BooleanField(null=True, blank=True)
        
    def __str__(self):
        return self.name

    @property
    def obtaine_tot_price_per_item(self):
        result = self.quantity*self.price
        return result

    @staticmethod
    def create_item_dict_from_response_post(response_post):
        item_dict = {}
        item_dict["name"] = response_post.get("name")
        item_dict["quantity"] = response_post.get("quantity")
        item_dict["price"] = response_post.get("price")
        item_dict["unit"] = response_post.get("unit")
        item_dict["item_type"] = response_post.get("item_type")
        item_dict["complete"] = False                
        return item_dict

    @classmethod
    def create(cls, slist, name, quantity, unit, item_type, price, complete):
        
        if len(name) < 2:
            raise ValueError("Name lenght must be at least 2 characters")
        
        if quantity == '':
            quantity = 0
        if price == '':
            price = 0
        
        try:
            int(quantity)
        except ValueError:
            raise ValueError("Quantity must be a integer")
        
        try:
            float(price)
        except ValueError: 
            raise ValueError("Price must be a float")
        
        return cls(slist=slist, name=name, quantity=quantity, unit=unit, item_type=item_type, price=price, complete=complete)

        
class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name="friends", null=True, blank=True, on_delete=models.CASCADE)
    
    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)
        
    @classmethod
    def delete_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)