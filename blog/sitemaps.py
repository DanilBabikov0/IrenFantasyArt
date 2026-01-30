# blog/sitemap.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost

class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'http'  # ← http для локальной разработки

    def items(self):
        return BlogPost.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class BlogStaticSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'
    protocol = 'http'  # ← http для локальной разработки

    def items(self):
        return ['blog_list']

    def location(self, item):
        return reverse(item)