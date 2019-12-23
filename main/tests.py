import time, datetime, json

from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from django.core import mail
# Create your tests here.
from .models import User, Post, Comment

class UserModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
                username='testuser', 
                password='password', 
                email='testuser@mail.com')

    def test_default_gender_value(self):
        self.assertEqual(self.user.gender, '0')

    def test_set_illegal_gender_value(self):
        with self.assertRaises(ValidationError):
            self.user.gender = 'M'
            self.user.clean_fields()

    def test_username_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            u2 = User.objects.create(username='testuser', password='password', email='anotheruser@mail.com')

    def test_email_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            u2 = User.objects.create(username='anotheruser', password='password', email='testuser@mail.com')


    def test_confirm_fails_when_token_expires(self):
        token = self.user.generate_confirmation_token(5)
        time.sleep(10)
        self.assertFalse(self.user.confirm(token))        

    def test_confirm_fails_when_use_another_user_token(self):
        u2 = User.objects.create(username='anotheruser',password='password',email='anotheruser@mail.com')
        token2 = u2.generate_confirmation_token(3600)
        self.assertFalse(self.user.confirm(token2))

    def test_confirm_succeed_when_use_token_in_time(self):
        self.assertFalse(self.user.confirmed)
        token = self.user.generate_confirmation_token()
        self.assertTrue(self.user.confirm(token))
        self.assertTrue(self.user.confirmed)

    def test_user_age(self):
        today = timezone.now().date()
        self.user.birthday = datetime.date(today.year-20,today.month,today.day)
        self.assertEqual(self.user.age(),20)
        if today.day != 1:
            self.user.birthday = datetime.date(today.year-20,today.month,today.day-1)
            self.assertEqual(self.user.age(),19)

    def test_user_birthmonth_false(self):
        self.user.birthday = datetime.date(2000,11,28)
        self.assertFalse(self.user.birthmonth())

    def test_user_birthmonth_true(self):
        self.user.birthday = datetime.date(2000,12,16)
        self.assertTrue(self.user.birthmonth())

    
class PostModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='hotkey', password='password',email='boom@shakalaka.com')
        cls.p1 = Post.objects.create(creator=cls.user, 
                created_at=timezone.now(), 
                published_at = timezone.now(),
                content=json.dumps({"title":"test p1 title"}))
        cls.p2 = Post.objects.create(creator=cls.user,
                created_at=timezone.now(), content=json.dumps({"intro":"test p2 intro"}))


    def test_get_title(self):
        self.assertEqual(self.p1.get_title(), 'test p1 title')
        self.assertIsNone(self.p2.get_title())

    def test_get_intro(self):
        self.assertEqual(self.p2.get_intro(),'test p2 intro')
        self.assertIsNone(self.p1.get_intro())

    def test_is_published(self):
        self.assertTrue(self.p1.is_published())
        self.assertFalse(self.p2.is_published())

    def test_creator_foreign_key(self):
        self.assertIn(self.p1, self.user.post_set.all())
        self.assertIn(self.p2, self.user.post_set.all())

    def test_foreign_key_delete_cascade(self):
        id1 = self.p1.id
        self.user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Post.objects.get(pk=id1)

class MainViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='jack', password=make_password('password'))

    def test_index_default(self):
        response = self.client.get('/')
        self.assertIn('items', response.context.keys())
        self.assertIn('page_of_paginator', response.context.keys())

    def test_login_index_all(self):
        ret = self.client.login(username='jack',password='password')
        self.assertTrue(ret)
        response = self.client.get('/?t=all')
        self.assertIn('query_string_prefix', response.context.keys())

    def test_register(self):
        response = self.client.post('/register', 
                {'username':'tommy','email':'tommy@fake.com','password':'secret', 'confirm_password':'secret'})
        self.assertEqual(len(mail.outbox), 1)
        u = User.objects.get(username='tommy')
        self.assertEqual(u.email, 'tommy@fake.com')
        ret = self.client.login(username='tommy', password='secret')
        self.assertTrue(ret)

    def test_profile_edit_redirect(self):
        response = self.client.get('/profile')
        self.assertRedirects(response, '/login?next=/profile')

    def test_get_profile_edit(self):
        self.client.login(username='jack', password='password')
        response = self.client.get('/profile')
        self.assertTemplateUsed(response, 'main/profile_edit.html')

    def test_post_create_redirect(self):
        response = self.client.get(reverse('post_create'))
        self.assertRedirects(response, reverse('login')+'?next='+reverse('post_create'))
        self.client.login(username='jack', password='password')
        response = self.client.get(reverse('post_create'))
        self.assertRedirects(response, reverse('unconfirmed')+'?next='+reverse('post_create'))

    def test_post_create_when_confirmed(self):
        self.user.confirmed = True
        self.user.save()
        self.client.login(username='jack', password='password')
        response = self.client.get(reverse('post_create'))
        self.assertTemplateUsed(response, 'post/create.html')

    def test_resend_confirmation_email(self):
        mail.outbox = []
        self.client.login(username='jack', password='password')
        response = self.client.get(reverse('unconfirmed'),HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # since user has not email addr, thus the email cannot be sent
        if len(mail.outbox) == 1:
            self.assertEqual(response.json()['sent'], True)
        else:
            self.assertEqual(response.json()['sent'], False)

