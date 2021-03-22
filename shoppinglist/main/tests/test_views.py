from django.test import TestCase, Client
from django.urls import reverse
from main.models import SList, Item
import json

# Testing only the the nouser app because to test main it is necessary to authenticate the user, and I not sure of how to do ir here
# To run th

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.nouser_home_url = reverse('nouser:nouserhome')
    
    def test_userhome_GET(self):
        
        response = self.client.get(self.nouser_home_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'nouser/nouserhome.html')