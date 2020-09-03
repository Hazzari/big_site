from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .form import EmailPostForm, CommentForm
from .models import Post, Comment


class PostListView(ListView):
    """
    # TODO: Вариант с использованием функций:

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

    # Список активных комментариев для этой статьи.
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # пользователь отправил комментарий.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в БД(commit=False).
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье.
            # TODO: удалить print
            print(f"post ================= {post}")
            new_comment.post = post
            # Сохраняем комментарий в базе данных.
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form})


def post_share(request, post_id):
    # Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data  # в словарь попадают только корректные поля
            # Отправка письма
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

    else:  # Вариант если GET отправляем пустую форму
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
