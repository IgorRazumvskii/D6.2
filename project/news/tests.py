from django.test import TestCase
from django.contrib.auth.models import User
from .models import *

# Create your tests here.
class TestModels(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='user1')
        self.author = Author.objects.create(rate=1, user=self.user)

    def test_authors(self):
        self.assertEqual(self.author.user.username, 'user1')
        self.assertEqual(self.author.rate, 1)

    def test_update_rating(self):
        #  self.assertEqual(self.author.update_rating())
        self.author.update_rating()
        print(self.author.rate)