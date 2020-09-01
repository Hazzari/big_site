from django.contrib import admin
from .models import Post


# Регистрация модели в админской панели
# 2 варианта:
# 1).
# admin.site.register(Post)
# 2).
@admin.register(Post)
class Admin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status',)
    list_filter = ('status', 'created', 'publish', 'author')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
