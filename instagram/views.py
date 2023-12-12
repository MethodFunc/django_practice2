import requests
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from instagram.forms import PostForm, CommentForm

from django.contrib import messages
from .models import Tag, Post

from django.utils import timezone
from datetime import timedelta


@login_required
def index_view(request):
    post_list = (Post.objects.all().filter(Q(author=request.user) |
                                           Q(author__in=request.user.following_set.all())
                                           )
                 .filter(create_dt__gte=timezone.now() - timedelta(days=3)).order_by('-create_dt'))

    suggested_user_list = (get_user_model().objects.all().exclude(pk=request.user.pk)
                           .exclude(pk__in=request.user.following_set.all())[:3])

    comment_form = CommentForm()
    return render(request, 'instagram/index.html', {
        "suggested_user_list": suggested_user_list,
        "post_list": post_list,
        "comment_form": comment_form
    })


# Create your views here.

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # 태그 분류
            post.tag_set.add(*post.extract_tag_list())

            messages.success(request, '새로운 글이 등록되었습니다.')
            return redirect(post)  # TODO: get_absolute_url use
    else:
        form = PostForm()

    return render(request, 'instagram/post_form.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()

    return render(request, 'instagram/post_detail.html',
                  {'post': post,
                   'comment_form': comment_form})


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post

            comment.save()

            return redirect(comment.post)

    else:
        form = CommentForm()

    return render(request, "instagram/comment_form.html",
                  {"form": form})


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)

    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    post_list_count = post_list.count()

    return render(request, 'instagram/user_page.html', {
        "page_user": page_user,
        "post_list": post_list,
        "post_list_count": post_list_count,
        "is_follow": is_follow,
    })


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)

    messages.success(request, '좋아요를 누르셨습니다.')

    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)

    messages.success(request, '좋아요를 취소하셨습니다.')
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)
