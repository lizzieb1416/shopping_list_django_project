from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import list_renderer, userhome, sort_list
from django.conf import settings

# To run tests: python manage.py test .\<app name>\

class TestUrls(SimpleTestCase):
   
   
    def test_list_renderer_url_resolves(self):
        #url = reverse('main:list_renderer', args=['(?P<id>[0-9]+)$'])
        #print(resolve(url))
        #self.assertEquals(resolve(url).func, list_renderer)
        pass
    
    def test_userhome_url_resolves(self):
        url = reverse('main:userhome')
        print(resolve(url))
        self.assertEquals(resolve(url).func, userhome)