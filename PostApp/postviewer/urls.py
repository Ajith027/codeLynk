from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.usercreate.as_view(), name='usercreate'),
    path('login/', views.userlogin.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='Logout'),
    path('posts/', views.All_posts.as_view(), name='All_post'),
    path('like/', views.To_likepost.as_view(), name='likepost'),
    path('unlike/', views.To_unlikepost.as_view(), name='unlikepost'),
    path('likedusers/', views.All_usersLiked.as_view(), name='likedusers'),

]
