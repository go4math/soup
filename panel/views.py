from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from main.models import Post, User, Comment
from utils import pagination_helper
# Create your views here.

@login_required
def panel_posts(request):
    
    object_list = request.user.post_set.filter(published_at__lt=timezone.now()).order_by('-created_at')
    
    page = request.GET.get('page',1)

    items, page_of_paginator = pagination_helper(object_list, page)

    return render(request, 'panel/posts.html',{'items': items,
        'page_of_paginator': page_of_paginator})

@login_required
def panel_drafts(request):

    object_list = request.user.post_set.exclude(published_at__lt=timezone.now()).order_by('-created_at')
    
    page = request.GET.get('page',1)

    items, page_of_paginator = pagination_helper(object_list, page)

    return render(request, 'panel/drafts.html',{'items': items,
        'page_of_paginator': page_of_paginator})

@login_required
def panel_comments_rcvd(request):
    
    posts = request.user.post_set.order_by('-created_at')
    object_list = Comment.objects.filter(post__in = posts
            ).exclude(creator__exact = request.user).order_by('-created_at')

    page = request.GET.get('page', 1)
    items, page_of_paginator = pagination_helper(object_list, page)
    return render(request, 'panel/comments_rcvd.html',{'items': items, 
        'page_of_paginator':page_of_paginator})

@login_required
def panel_comments_sent(request):

    object_list = Comment.objects.filter(creator=request.user).order_by('-created_at')

    page = request.GET.get('page', 1)
    items, page_of_paginator = pagination_helper(object_list, page)
    return render(request, 'panel/comments_sent.html',{'items': items,
        'page_of_paginatior': page_of_paginator})

@login_required
def panel_users_followed_by_me(request):

    object_list = request.user.follow.exclude(id__exact=request.user.id)

    page = request.GET.get('page', 1)
    items, page_of_paginator = pagination_helper(object_list, page)
    return render(request, 'panel/users_followed_by_me.html',{'items': items,
        'page_of_paginator': page_of_paginator})

@login_required
def panel_users_following_me(request):

    object_list = request.user.fans.exclude(id__exact=request.user.id)

    page = request.GET.get('page', 1)
    items, page_of_paginator = pagination_helper(object_list, page)
    return render(request, 'panel/users_following_me.html',{'items': items,
        'page_of_paginator': page_of_paginator})
