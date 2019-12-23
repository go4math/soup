from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile_edit, name='profile_edit'),
    path('confirm/<str:token>', views.confirm, name='confirm'),
    path('unconfirmed/', views.unconfirmed, name='unconfirmed'),
]
