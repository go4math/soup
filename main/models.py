import hashlib
import json
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from soup.settings import SECRET_KEY as sk

class User(AbstractUser):

   # class Gender(models.TextChoices):
   #     OTHER = '0', _('其他')
   #     MALE = '1', _('男')
   #     FEMALE = '2', _('女')
    GENDER = [('1','男'),('2','女'),('0','其他')]

    email = models.EmailField('email', unique=True)

    name = models.CharField('name', max_length=30, blank=True)
    bio = models.TextField('bio', max_length=200, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, default='0')
    birthday = models.DateField('birthday', blank=True, null=True)
    location = models.CharField('location', blank=True, max_length=40)

    follow = models.ManyToManyField('self', symmetrical=False, related_name="fans")

    confirmed = models.BooleanField(default=False)

    def gravatar(self, size=50, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return '{url}/{hash}/?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def gravatar100(self):
        return self.gravatar(size=100)
    def gravatar200(self):
        return self.gravatar(size=200)

    def age(self):
        if self.birthday is not None:
            dy = timezone.now().date().year - self.birthday.year
            dm = timezone.now().date().month- self.birthday.month
            dd = timezone.now().date().day - self.birthday.day
            if dm > 0:
                a = dy - 1
            elif dm < 0:
                a = dy
            else:
                a = dy-1 if dd > 0 else dy
         
            return a
        else:
            return None
    
    def birthmonth(self):
        return timezone.now().date().month == self.birthday.month

    def get_url(self):
        return '/user/'+self.username

    def generate_confirmation_token(self, expiration=86400): # default is 24 hrs
        s = Serializer(sk, expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')
        

    def confirm(self, token):
        s = Serializer(sk)
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') == self.id:
            self.confirmed = True
            self.save()
            return True


class Post(models.Model):
    #class Type(models.TextChoices):
    #    RECIPE = 'R', _('recipe')
    #    COOKED = 'C', _('cooked')
    TYPE = [('R','recipe'),('C','cooked')]

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=1, choices=TYPE)
    created_at = models.DateTimeField('created_at', default=timezone.now)
    published_at = models.DateTimeField('published_at', blank=True, null=True)
    content = models.TextField('content')

    def get_url(self):
        return '/post/'+str(self.id)+'/'

    def is_published(self):
        return self.published_at and self.published_at < timezone.now()

    def get_title(self):
        try:
            t = json.loads(self.content)["title"]
            return t
        except:
            return None


    def get_intro(self):
        try:
            intro = json.loads(self.content)["intro"]
            return intro
        except:
            return None

class Comment(models.Model):
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField('content', default="Awesome cherry mango dance")
    created_at = models.DateTimeField('created_at', default=timezone.now)

    def get_url(self):
        # like '/post/6/#13'
        return '/post/'+str(self.post.id)+'/#c'+str(self.id)
