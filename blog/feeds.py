from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

# Feed - подсистема фидов Django
class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    def items(self):
        # Объекты которые включены в рассылку
        return Post.published.all()[:5]

    def item_title(self, item):
        # получает заголовок от каждого элемента из результата заголовок
        return item.title

    def item_description(self, item):
        # получает заголовок от каждого элемента из результата описание с фильтром в 30 слов
        return truncatewords(item.body, 30)
