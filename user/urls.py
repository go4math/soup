from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/', views.user_view, name='user_view'),
    path('follow/<str:username>', views.user_follow, name='user_follow'),
    path('unfollow/<str:username>', views.user_unfollow, name='user_unfollow'),
    path('remove/<str:username>', views.user_remove_fan, name='user_remove_fan'),
]
