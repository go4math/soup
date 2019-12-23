from django.test import TestCase

# Create your tests here.

# test post/views.py
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from main.models import User, Post, Comment

class ViewTests(TestCase):

    def setUp(self):
        self.author  = User.objects.create(username='author', password=make_password('secret'),
                email='author@fake.com')
        self.viewer = User.objects.create(username='viewer', password=make_password('secret'),
                email='viewer@fake.com')
        self.post = Post(creator=self.author, published_at = timezone.now(), content="{}")
        self.draft = Post(creator=self.author,content="{}")
        self.post.save()
        self.draft.save()

    def test_author_view_post(self):
        self.client.login(username='author', password='secret')
        response = self.client.get(reverse('post_view', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_author_view_draft(self):
        self.client.login(username='author', password='secret')
        response = self.client.get(reverse('post_view', args=[self.draft.id]))
        self.assertEqual(response.status_code, 200)

    def test_viewer_view_post(self):
        self.client.login(username='viewer', password='secret')
        response = self.client.get(reverse('post_view', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_viewer_view_draft(self):
        self.client.login(username='viewer', password='secret')
        response = self.client.get(reverse('post_view', args=[self.draft.id]))
        self.assertEqual(response.status_code, 404)

    def test_author_edit_post(self):
        self.client.login(username='author', password='secret')
        response = self.client.get(reverse('post_edit', args=[self.post.id]))
        self.assertRedirects(response, reverse('post_view', args=[self.post.id]))

    def test_author_edit_draft(self):
        self.client.login(username='author', password='secret')
        response = self.client.get(reverse('post_edit', args=[self.draft.id]))
        self.assertTemplateUsed(response, 'post/edit.html')

    def test_viewer_edit_permission_denied(self):
        self.client.login(username='viewer', password='secret')
        response = self.client.get(reverse('post_edit', args=[self.draft.id]))
        self.assertEqual(response.status_code, 403)

    def test_comment_create_unconfirmed_redirect(self):
        self.client.login(username='viewer', password='secret')
        response = self.client.post(reverse('post_comment_create',args=[self.post.id]), {})
        self.assertRedirects(response, reverse('unconfirmed')+'?next='+reverse('post_comment_create', args=[self.post.id]))

    def test_comment_create_confirmed(self):
        self.viewer.confirmed = True
        self.viewer.save()
        self.client.login(username='viewer', password='secret')
        response = self.client.post(reverse('post_comment_create', args=[self.post.id]), {'comment': 'ruin my life'})
        self.assertRedirects(response, reverse('post_view', args=[self.post.id]))

    def test_comment_create_on_draft(self):
        self.client.login(username='viewer', password='secret')
        self.viewer.confirmed = True
        self.viewer.save()
        response = self.client.post(reverse('post_comment_create', args=[self.draft.id]), {'comment': 'ruin my life'})
        self.assertEqual(response.status_code, 404)
        
    def test_comment_delete(self):
        author_comment = Comment.objects.create(creator=self.author, post = self.post, content="author comment")
        viewer_comment1 = Comment.objects.create(creator=self.viewer, post = self.post, content = "viewer comment 1")
        viewer_comment2 = Comment.objects.create(creator=self.viewer, post = self.post, content = "viewer comment 2")
        author_comment.save()
        viewer_comment1.save()
        viewer_comment2.save()
        self.client.login(username='viewer',password='secret')
        response = self.client.get(reverse('post_comment_delete', args=[author_comment.id]))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('post_comment_delete', args=[viewer_comment1.id]))
        self.assertRedirects(response, reverse('index'))

        self.client.login(username='author', password='secret')
        response = self.client.get(reverse('post_comment_delete', args=[viewer_comment2.id]))
        self.assertRedirects(response, reverse('index'))

    def test_view_comments(self):

        self.client.login(username='viewer', password='secret')
        response = self.client.get(reverse('post_view_comments', args=[self.draft.id]))
        self.assertEqual(response.status_code, 404)


        response = self.client.get(reverse('post_view_comments', args=[self.post.id]))
        self.assertTemplateUsed(response, 'post/view_comments.html')







    

    
    
