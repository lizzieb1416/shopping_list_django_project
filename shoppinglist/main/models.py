from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# PRODUCT_TYPE_CHOICES = (
#     ('fruit', 'FRUIT'),
#     ('vegetable', 'VEGETABLE'),
#     ('dairy', 'DAIRY'),
#     ('meat', 'MEAT'),
#     ('grain', 'GRAIN'),
#     ('other', 'OTHER'),
# 

class SList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="slist", null=True, blank=True)
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
        unity = ""
        item_type = response_post.get("item_type")
        price = response_post.get("price")
        complete = False 
        
        item_created = Item.create(slist, name=name, quantity=quantity, unity=unity, item_type=item_type, price=price, complete=complete)
        item_created.save()            

            
   
    
class Item(models.Model):
    slist = models.ForeignKey(SList, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    quantity = models.IntegerField(max_length=100, blank=True)
    unity = models.CharField(max_length=100, blank=True)
    item_type = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=30, decimal_places=2, blank=True)
    complete = models.BooleanField(null=True, blank=True)
        
    def __str__(self):
        return self.name

    @staticmethod
    def create_item_dict_from_response_post(response_post):
        item_dict = {}
        item_dict["name"] = response_post.get("name")
        item_dict["quantity"] = response_post.get("quantity")
        item_dict["price"] = response_post.get("price")
        item_dict["item_type"] = response_post.get("item_type")
        item_dict["complete"] = False                
        return item_dict

    @classmethod
    def create(cls, slist, name, quantity, unity, item_type, price, complete):
        
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
        
        return cls(slist=slist, name=name, quantity=quantity, unity=unity, item_type=item_type, price=price, complete=complete)

        
        

    # def set_name(self, value):
    #     if len(value) >= 2:
    #         self.name = value
    #     else:
    #         messages.add_message(response, messages.ERROR, "Name must be more than 1 letter")            

    # def set_quantity(self, value):
    #     if value == '':
    #         self.quantity = 0
    #     else:
    #         try:
    #             self.quantity = int(value)
    #         except:
    #             messages.add_message(response, messages.ERROR, "Quantity must be integer")
                                
    # def set_price(self, value):
    #     if value == '':
    #         self.price = 0
    #     else:
    #         try:
    #             self.price = float(value)
    #         except:
    #             messages.add_message(response, messages.ERROR, "Price must be float")
                
    
