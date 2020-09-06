from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post

# Регистрация своих тегов происходит через экземпляр Library
register = template.Library()


# Регистрируем тег
@register.simple_tag
def total_posts():
    """
    Возвращаем количество статей.

    :return: QuerySet
    """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_posts(count=5):
    """
    последние статьи

    :param count: количество статей.
    :return: dict
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    # annotate() - добавляем к каждой статье количества комментариев.
    # Count - используется в качестве функции агрегации,
    # которая вычисляет количество комментариев total_comments
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
