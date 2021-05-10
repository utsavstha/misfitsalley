from django.shortcuts import render, redirect
from core.models import *
import hashlib
from django.db.models import F


def posts(request):
    query = '''
            SELECT core_posts.id, core_posts.title, core_posts.content, 
            core_posts.createdAt, core_posts.flags, auth_user.username, 
            core_category.name, 
            (SELECT COUNT(core_comment.id) FROM core_comment WHERE core_comment.post_id = core_posts.id) as comments,  
            (SELECT COUNT(core_likes.id) FROM core_likes WHERE core_likes.post_id = core_posts.id) as likes,  
            (SELECT COUNT(core_dislikes.id) FROM core_dislikes WHERE core_dislikes.post_id = core_posts.id) as dislikes 
            FROM core_posts 
            JOIN core_category ON core_posts.category_id = core_category.id 
            JOIN auth_user ON core_posts.user_id = auth_user.id 
            '''
    posts = Posts.objects.raw(query)
    user = None
    imagehash = None
    if request.user != "AnonymousUser":
        user = request.user
        imagehash = hashlib.md5((user.username).encode('utf-8'))
    print(posts[0])
    context = {'posts': posts, 'user': user,
               'imagehash': imagehash.hexdigest()}
    return render(request, 'post/posts.html', context)


def viewPost(request, pk):
    post = Posts.objects.get(id=pk)
    likes = post.likes_set.all()
    dislikes = post.dislikes_set.all()
    comments = post.comment_set.all()
    user = None
    imagehash = None
    if request.user != "AnonymousUser":
        user = request.user
        print(user.id)
        imagehash = hashlib.md5((user.username).encode('utf-8'))

    context = {'post': post, 'comments': comments,
               'imagehash': imagehash.hexdigest(), 'likes': len(likes), 'dislikes': len(dislikes)}
    return render(request, 'post/view_post.html', context)


def createPost(request):
    categories = Category.objects.all()
    tags = Tags.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        formTags = request.POST.getlist('tags')
        content = request.POST.get('content')
        post = Posts(title=title, category=Category.objects.get(id=category),
                     content=content, user=request.user, flags=0)
        post.save()
        for tag in formTags:
            post.tags.add(Tags.objects.get(id=tag))
        return redirect('posts')
    context = {'categories': categories, 'tags': tags}
    return render(request, 'post/create_post.html', context)


def postComment(request, pk):
    post = Posts.objects.get(id=pk)
    content = request.POST.get('content')

    comment = Comment(user=request.user, post=post,
                      content=content, likes=0, dislikes=0, flags=0)
    comment.save()
    return redirect('view_post', pk=pk)


def postLike(request, pk):
    post = Posts.objects.get(id=pk)
    like = Likes.objects.filter(user=request.user, post=post)
    if like:
        return redirect('view_post', pk=pk)
    else:
        newLike = Likes(user=request.user, post=post)
        newLike.save()
        return redirect('view_post', pk=pk)


def postDisLike(request, pk):
    post = Posts.objects.get(id=pk)
    dislike = Dislikes.objects.filter(user=request.user, post=post)
    if dislike:
        return redirect('view_post', pk=pk)
    else:
        newDislike = Dislikes(user=request.user, post=post)
        newDislike.save()
        return redirect('view_post', pk=pk)
