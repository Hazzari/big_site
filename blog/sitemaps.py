from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    # частота обновления страниц статей и степень их совпадения с тематикой сайта (max=1)
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        # обьекты которые будут отображатся в карте сайта
        return Post.published.all()

    def lastmod(self, obj):
        # принимает каждый обьект из items и возвращает время последней модификации статьи
        return obj.updated
