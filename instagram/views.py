from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from instagram.forms import PostForm

from django.contrib import messages
from .models import Tag, Post

import pickle as pk


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
    return render(request, 'instagram/post_detail.html',
                  {'post': post})
