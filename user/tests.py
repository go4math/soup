from django.test import TestCase

# Create your tests here.
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from main.models import User

class ViewTests(TestCase):

    def setUp(self):

        self.me = User.objects.create(username='me', password=make_password('secret'),
                email = 'me@fake.com')

        self.susie = User.objects.create(username='susie', password='secret', email='susie@fake.com')

        self.me.save()
        self.susie.save()

    def test_user_view(self):
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('user_view', args=['susie']))
        self.assertTemplateUsed(response, 'user/view.html')

    def test_user_follow(self):
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('user_follow', args=['susie']))
        self.assertIn("followed", response.json())

    def test_user_unfollow(self):
        self.me.follow.add(self.susie)
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('user_unfollow', args=['susie']))
        self.assertIn('unfollowed', response.json())

    def test_user_remove(self):
        self.susie.follow.add(self.me)
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('user_remove_fan', args=['susie']))
        self.assertIn("removed", response.json())
        
