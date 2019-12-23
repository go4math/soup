from django.test import TestCase

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.urls import reverse
# Create your tests here.
from main.models import User, Post, Comment

class ViewTests(TestCase):

    def setUp(self):
        self.me = User.objects.create(username='me',password=make_password('secret'),
                email = 'me@fake.com')
        self.idol = User.objects.create(username='idol', password='secret', email = 'idol@fake.com')
        self.fan = User.objects.create(username='fan', password='secret', email='fan@fake.com')
        self.me.save()
        self.idol.save()
        self.fan.save()

        self.my_post = Post(creator=self.me, published_at = timezone.now(), content="{}")
        self.my_draft = Post(creator=self.me, content="{}")
        self.my_post.save()
        self.my_draft.save()

        self.idol_post = Post(creator=self.idol, published_at = timezone.now(), content="{}")
        self.idol_post.save()

        self.comment_sent = Comment(creator=self.me, post = self.idol_post, content="ruin my life")
        self.comment_rcvd = Comment(creator=self.fan, post = self.my_post, content="awesome!")
        self.comment_sent.save()
        self.comment_rcvd.save()

        self.me.follow.add(self.idol)
        self.me.fans.add(self.fan)
        self.me.save()


    def test_panel_posts(self):
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('panel_posts'))
        p = response.context["items"][0]
        self.assertEqual(p.id, self.my_post.id)

    def test_panel_drafts(self):
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('panel_drafts'))
        p = response.context["items"][0]
        self.assertEqual(p.id, self.my_draft.id)

    def test_comments_rcvd(self):
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('panel_comments_rcvd'))
        p = response.context["items"][0]
        self.assertEqual(p.id, self.comment_rcvd.id)

    def test_comments_sent(self):
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('panel_comments_sent'))
        p = response.context["items"][0]
        self.assertEqual(p.id, self.comment_sent.id)

    def test_users_followed_by_me(self):
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('panel_users_followed_by_me'))
        p = response.context["items"][0]
        self.assertEqual(p.id, self.idol.id)

    def test_users_following_me(self):
        self.client.login(username='me', password='secret')
        response = self.client.get(reverse('panel_users_following_me'))
        p = response.context["items"][0]
        self.assertEqual(p.id, self.fan.id)




