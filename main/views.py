from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import QueryDict, JsonResponse
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
#from django.template.loader import render_to_string
from django.contrib import messages

# Create your views here.

from .forms import loginForm, registryForm, profileForm
from .models import User, Post, Comment
from utils import pagination_helper, send_confirmation_mail

from soup.settings import BASE_URL

def index_view(request):
    t = request.GET.get('t', None)
    if request.user.is_authenticated and t == 'all':

        p = Post.objects.filter(published_at__lt=timezone.now()).order_by('-published_at')
        page = request.GET.get('page', 1)
        posts, page_of_paginator = pagination_helper(p, page, 5)

        query_string_prefix="t=all&"
        return render(request, 'main/index_all.html', {'items': posts, 
            'query_string_prefix': query_string_prefix, 'page_of_paginator':page_of_paginator})

    elif request.user.is_authenticated: 
        
        # default is showing posts of whom the user is following
        u = request.user.follow.all()
        p = Post.objects.filter(published_at__lt=timezone.now()).filter(
            creator__in=u).order_by('-published_at')
        page = request.GET.get('page', 1)
        posts, page_of_paginator = pagination_helper(p, page, 5)
        return render(request, 'main/index.html', {'items': posts,
            'page_of_paginator': page_of_paginator})

    else:
        # provide limited number(20) of posts to anonymous user
        p = Post.objects.filter(published_at__lt=timezone.now()).order_by('-published_at')[:15]
        page = request.GET.get('page', 1)
        posts, page_of_paginator = pagination_helper(p, page, 5)
        return render(request, 'main/index_all.html', {'items': posts,
            'page_of_paginator': page_of_paginator})



def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = loginForm(request.POST)
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        user = authenticate(username=identifier, password=password)
        if user is not None:
            login(request,user)
            next_url = QueryDict(request.META['QUERY_STRING']).get('next', None)
            if next_url is not None:
                return redirect(next_url)
            else:
                return redirect(reverse('index'))
        else:
            form.add_error(None, '登录名或密码不正确.')
            return render(request, 'main/login.html', {'form': form})
    else:
        form = loginForm(label_suffix='')
        return render(request, 'main/login.html', {'form':form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        form = registryForm(request.POST)
        if form.is_valid():
            
            try:
                user = User(
                    username = form.cleaned_data.get('username'),
                    email = form.cleaned_data.get('email'),
                    password = make_password(form.cleaned_data.get('password')),
                 )
                user.save()
                res = send_confirmation_mail(user)
            
            # token = user.generate_confirmation_token(86400)
            # confirmation_link = 'http://'+BASE_URL+'confirm/'+token
            # msg = "{}, 你好!\n感谢你的注册, 请在24小时内点击下面链接确认你的邮箱:\n{}\nSoup Team 致敬".format(user.username, confirmation_link)
            # html_msg = render_to_string('mail/confirmation.html',{'name': user.username, 'link':confirmation_link})
            # send_mail('请确认你的邮箱',msg,
                    # 'pjltest@outlook.com',[user.email], html_message=html_msg)"""
                if res:
                    messages.success(request,"我们将会发送一封确认邮件至您的邮箱, 请您24小时之内确认.")
                else:
                    pass
            except:
                messages.error(request,"很抱歉, 账户未能成功创建, 请您稍后再试.")
            return redirect(reverse('login'))
        else:
            return render(request, 'main/register.html', {'form': form})

    else:
        form = registryForm(label_suffix='')
        return render(request, 'main/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

@login_required
def profile_edit(request):
    if request.method == "POST":
        form = profileForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            request.user.bio = form.cleaned_data['bio']
            request.user.name = form.cleaned_data['name']
            request.user.gender = form.cleaned_data['gender']
            request.user.birthday = form.cleaned_data['birthday']
            province = request.POST["province"]
            city = request.POST["city"]
            request.user.location = province + "-" + city
            request.user.save(update_fields=['bio','name','gender','birthday','location'])
            messages.success(request, '信息更新成功.')
            return render(request, 'main/profile_edit.html', {'form': form, 'province': province,'city':city})
        else:
            province, city = request.user.location.split("-")
            return render(request, 'main/profile_edit.html', {'form': form, 'province': province, 'city':city})
            
    else:
        try:
            province, city = request.user.location.split("-")
        except ValueError:
            province = "0"
            city = "0"
        form = profileForm(initial={
            'bio': request.user.bio,
            'name': request.user.name,
            'gender': request.user.gender,
            'birthday': request.user.birthday,
            #'location': request.user.location
        }, label_suffix='')

        return render(request, 'main/profile_edit.html', {'form': form, 
            'province': province, 'city':city})


@login_required
def confirm(request, token):
    confirmed = request.user.confirm(token)
    if confirmed:
        messages.success(request, "你的邮箱已确认!")
        return redirect(reverse('index'))
    else:
        messages.error(request, "很抱歉链接无效, 无法确认你的邮箱.")
        return redirect(reverse('index_all'))

@login_required
def unconfirmed(request):
    if request.is_ajax():
        '''user = request.user
        token = user.generate_confirmation_token(86400)
        confirmation_link = 'http://'+BASE_URL+'confirm/'+token
        msg = "{}, 你好!\n感谢你的注册, 请在24小时内点击下面链接确认你的邮箱:\n{}\nSoup Team 致敬".format(user.username, confirmation_link)
        html_msg = render_to_string('mail/confirmation.html',{'name': user.username, 'link':confirmation_link})
        res = send_mail('请确认你的邮箱',msg,
                'pjltest@outlook.com',[user.email], html_message=html_msg)
        '''
        res = send_confirmation_mail(request.user)

        if res:
            return JsonResponse({"sent":True})
        else:
            return JsonResponse({"sent":False})
    else:
        return render(request, 'main/unconfirmed.html')
