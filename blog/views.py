from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    # получаем все записи из базы данных (применяя менеджер модели получаем только 'published')
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    # возвращает 404 если объект не найден
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})
