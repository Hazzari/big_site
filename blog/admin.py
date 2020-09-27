from django.contrib import admin
from .models import Post, Comment


# Регистрация модели в админской панели
# 2 варианта:
# 1).
# admin.site.register(Post)
# 2).
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Отображает заголовки колонок
    list_display = ('title', 'slug', 'author', 'publish', 'status',)
    # Добавляет сбоку фильтр по категориям
    list_filter = ('status', 'created', 'publish', 'author')
    # Заполнять slug автоматом из поля title
    prepopulated_fields = {'slug': ('title',)}
    # выбрать автора по поиску
    raw_id_fields = ('author',)
    # дата сверху мелкой строкой
    date_hierarchy = 'publish'
    # умолчальная сортировка
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
