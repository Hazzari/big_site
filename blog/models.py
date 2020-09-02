from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


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
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])

    class Meta:
        # Порядок сортировки статей убывающий (последние будут первыми)
        ordering = ('-publish',)

    def __str__(self):
        # Для админки
        return self.title

    def __repr__(self):
        return self.title
