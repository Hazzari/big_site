from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager


class PublishManager(models.Manager):
    # Менеджер модели по умолчанию для .all()
    def get_queryset(self):
        # делаем фильтрованный запрос
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    # Список статусов
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликована'),
    )

    tags = TaggableManager()

    # Заголовок статьи
    title = models.CharField(max_length=50)
    # Для формирования уникальный URL
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # внешний ключ. один ко многим, удаление вместе с записями, обратная связь User to Post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    # содержание статьи
    body = models.TextField()
    # Дата публикации текущие дата и время с учетом временной зоны.
    publish = models.DateTimeField(default=timezone.now)
    # указатель на то когда была создана, указывается автоматически при создании объекта
    created = models.DateTimeField(auto_now_add=True)
    # -||- когда была отредактирована, при сохранении автообновляется
    updated = models.DateTimeField(auto_now=True)
    # статус статьи ( на выбор 2 варианта
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='draft')
    # Менеджер по умолчанию
    objects = models.Manager()
    # Новый менеджер published
    published = PublishManager()

    def get_absolute_url(self):
        b = Post.objects.get(pk=self.pk).created.astimezone(timezone.get_current_timezone())
        return reverse('blog:post_detail', args=[b.year,
                                                 b.month,
                                                 b.day,
                                                 self.slug])

    class Meta:
        # Порядок сортировки статей убывающий (последние будут первыми)
        ordering = ('-publish',)

    def __str__(self):
        # Для админки
        return self.title

    def __repr__(self):
        return self.title


class Comment(models.Model):
    # для привязки к определенной статье ( один ко многим) одна статья может иметь множество комментариев,
    # но каждый комментарий может быть оставлен только к одной статье.
    # related_name - для обращения по post.comments.all() ( по default = _set, comment_set)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # для скрытия некоторых комментариев
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
