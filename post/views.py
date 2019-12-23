import json
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import PermissionDenied 
from django.http import Http404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
from main.models import User, Post, Comment
from utils import confirm_required

@login_required
def post_view(request, pid):
    p = get_object_or_404(Post, pk=pid)

    if request.user == p.creator or (p.published_at and p.published_at < timezone.now()):
        post = json.loads(p.content)
        comment_count = p.comment_set.count()
        comments = p.comment_set.order_by('-created_at')[:3] # show only the latest 3 comments
        following = p.creator in request.user.follow.all()

        return render(request, 'post/view.html',{
            'display_user': p.creator,
            'post': p,
            'content': json.loads(p.content),
            'comments': comments,
            'comment_count': comment_count,
        })
    else:
        raise Http404("Post does not exist.")
    

@login_required
@confirm_required(login_url='/unconfirmed/')
def post_create(request):
    if request.method == "POST":
        do = request.POST.get('do')
        if do == 'del':
            return redirect(reverse('index'))

        # handle ingredient table
        items = []
        for i, q in zip(request.POST.getlist('item'), request.POST.getlist('quantity')):
            items.append({'item':i, 'quantity':q})

        post = {
            'title': request.POST.get('post-title'),
            'intro': request.POST.get('post-intro'),
            'items': items,
            'steps': request.POST.getlist('post-step'),
            'fyi': request.POST.get('post-fyi'),
        }
        
        if do == 'pub':
            p = Post(creator=request.user, post_type='R', published_at=timezone.now, 
                    content=json.dumps(post))
        else: # sav
            p = Post(creator=request.user, post_type='R', content=json.dumps(post))
        p.save()
        return redirect(reverse('post_view', args=[p.id]))

    else:
        return render(request, 'post/create.html')

@login_required
def post_edit(request, pid):
    p = get_object_or_404(Post, pk=pid)
    if p.is_published() : # after publish, even the author cannot edit
        return redirect(reverse('post_view', args=[pid]))
    
    if request.user == p.creator:
        post = json.loads(p.content)
        if request.method == "POST":
            do = request.POST.get('do')
            if do == 'del':
                return redirect(reverse('post_delete', args=[pid]))
            # handle ingredient table
            items = []
            for i, q in zip(request.POST.getlist('item'), request.POST.getlist('quantity')):
                items.append({'item':i, 'quantity':q})

            updated_post = {
                'title': request.POST.get('post-title'),
                'intro': request.POST.get('post-intro'),
                'items': items,
                'steps': request.POST.getlist('post-step'),
                'fyi': request.POST.get('post-fyi'),
            }            
            p.content = json.dumps(updated_post)

            if do == 'pub':
                p.published_at = timezone.now()
                p.save(update_fields=["content","published_at"])
            else: # do == 'sav'
                p.save(update_fields=["content"])
                
            return redirect(reverse('post_view', args=[pid]))

        else:
            return render(request, 'post/edit.html', {'post': post, 'pid':pid})
    else:
        raise PermissionDenied

@login_required
def post_delete(request, pid):
    p = get_object_or_404(Post, pk=pid)
    if request.user == p.creator:
        p.delete()
        return redirect(reverse('index'))
    else:
        raise PermissionDenied

@login_required
def post_save(request, pid):
    pass

@login_required
def post_publish(request, pid):
    pass

@login_required
@confirm_required(login_url="/unconfirmed/")
def post_comment_create(request, pid):
    # post is the only possible method for this view
    post = get_object_or_404(Post, pk=pid)

    if not post.is_published():
        raise Http404("Associated post does not exist.")
        return redirect(reverse('index'))

    content = request.POST.get('comment')
    replyto = re.match(r'@\w+', content)
    if replyto is not None:
        replyto = replyto.group()
#   we should save raw text
#   content = '<a href=\"/user/'+replyto[1:]+'\" class=\"orange-text\">'+replyto+'</a>'+content[len(replyto):]
    c = Comment(creator=request.user, post=post, content=content)
    c.save()
    return redirect(reverse('post_view', args=[pid]))

@login_required
def post_comment_delete(request, cid):
    c = get_object_or_404(Comment, pk=cid)
    next_url = request.META.get("HTTP_REFERER", None)
    
    if request.user not in (c.creator, c.post.creator):
        raise PermissionDenied

    try:
        c.delete()
        if next_url:
            messages.success(request, "评论删除成功!")
            return redirect(next_url)
        else:
            messages.success(request, "评论删除成功!")
            return redirect(reverse('index')) 
    except:
        messages.error(request, "评论删除失败!")
        return redirect(reverse('index'))


def post_view_comments(request, pid):
    
    p = get_object_or_404(Post, pk=pid)
    
    if not p.is_published():
        raise Http404("Post does not exist.")

    c = p.comment_set.order_by('-created_at')
    paginator = Paginator(c, 2) # TODO
    page = request.GET.get('page', 1)
    comments = paginator.get_page(page)

    paginator_of_paginator=Paginator(paginator.page_range,10)
    page_of_paginator = paginator_of_paginator.get_page((int(page)-1)//10+1)
    return render(request, 'post/view_comments.html', {'items': comments, 'post':p,
        'page_of_paginator': page_of_paginator})
