from django.urls import path

from . import views

urlpatterns = [
    path('<int:pid>/', views.post_view, name='post_view'),
    path('<int:pid>/edit', views.post_edit, name='post_edit'),
    path('<int:pid>/delete', views.post_delete, name='post_delete'),
    path('create', views.post_create, name='post_create'),
    path('<int:pid>/save', views.post_save, name='post_save'),
    path('<int:pid>/publish', views.post_publish, name='post_publish'),
    path('<int:pid>/comment/create', views.post_comment_create, name='post_comment_create'),
    path('comment/<int:cid>/delete', views.post_comment_delete, name='post_comment_delete'),
    path('<int:pid>/comments/', views.post_view_comments, name='post_view_comments'),
]
