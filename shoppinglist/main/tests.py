from django.test import TestCase

# from myapp.models import Animal

class AnimalTestCase(TestCase):
    def setUp(self):
        pass
        

    def test_animals_can_speak(self):
        self.assertTrue(True)
        
    def test_numbers(self):
        self.assertEquals('foo'.upper(), 'FOO')
        