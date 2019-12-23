from django.urls import path

from . import views

urlpatterns = [
    path('', views.panel_posts, name='panel_posts'),
    path('drafts/', views.panel_drafts, name='panel_drafts'),
    path('comments/', views.panel_comments_rcvd, name='panel_comments_rcvd'),
    path('comments/sent/', views.panel_comments_sent, name='panel_comments_sent'),
    path('users/', views.panel_users_followed_by_me, name='panel_users_followed_by_me'),
    path('users/fans/', views.panel_users_following_me, name='panel_users_following_me'),
]
