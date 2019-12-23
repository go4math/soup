from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone

from main.models import User
from utils import pagination_helper

# Create your views here.
def user_view(request, username):
    u = get_object_or_404(User, username=username)
    all_posts = u.post_set.filter(published_at__lt=timezone.now()).order_by('-created_at')

    page = request.GET.get('page', 1)
    posts, page_of_paginator = pagination_helper(all_posts, page, 5)


    return render(request, 'user/view.html', {'display_user':u, 'items': posts,
        'page_of_paginator': page_of_paginator})

def user_follow(request, username):
    try:
        u = User.objects.get(username=username)
        request.user.follow.add(u)
        return JsonResponse({"followed": True})
    except:
        return JsonResponse({"followed": False})

def user_unfollow(request, username):
    try:
        u = User.objects.get(username=username)
        request.user.follow.remove(u)
        return JsonResponse({"unfollowed": True})
    except:
        return JsonResponse({"unfollowed": False})
    
def user_remove_fan(request, username):
   try:
       u = User.objects.get(username=username)
       request.user.fans.remove(u)
       return JsonResponse({"removed":True})
   except:
       return JsonResponse({"removed":False})
