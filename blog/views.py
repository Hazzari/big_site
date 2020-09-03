from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    """
    # TODO: Вариант в функциональном стиле:

    # def post_list(request):
    #     # получаем все записи из базы данных
    #     # (применяя менеджер модели получаем только 'published')
    #     object_list = Post.published.all()
    #     paginator = Paginator(object_list, 3)  # по 3 статьи на каждой странице
    #
    #     # Получаем номер строки из - url
    #     page = request.GET.get('page')
    #
    #     try:
    #         posts = paginator.page(page)
    #     except PageNotAnInteger:
    #         # Если страница не является целым числом, возвращаем первую страницу.
    #         posts = paginator.page(1)
    #     except EmptyPage:
    #         # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю страницу.
    #         posts = paginator.page(paginator.num_pages)
    #     return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

    """
    # Используем переопределенный менеджер модели, для получения обычного
    queryset = Post.published.all()  # ListView
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'



def post_detail(request, year, month, day, post):
    # возвращает 404 если объект не найден
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})
