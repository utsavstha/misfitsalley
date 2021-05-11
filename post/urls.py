from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.posts, name="posts"),
    path('posts/<str:limit>/<str:offset>', views.posts, name="posts"),
    path('view_post/<str:pk>', views.viewPost, name="view_post"),
    path('create_post/', views.createPost, name="create_post"),
    path('comment/<str:pk>', views.postComment, name="post_comment"),
    path('like/<str:pk>', views.postLike, name="post_like"),
    path('dislike/<str:pk>', views.postDisLike, name="post_dislike"),

]
