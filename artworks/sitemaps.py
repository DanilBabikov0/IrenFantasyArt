# artworks/sitemap.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Artwork, Collection

class ArtworkSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'http' # ← http для локальной разработки

    def items(self):
        return Artwork.objects.filter(status='available')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CollectionSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'http'  # ← http для локальной разработки

    def items(self):
        return Collection.objects.all()

    def lastmod(self, obj):
        artworks = obj.artwork_set.order_by('-updated_at')
        return artworks.first().updated_at if artworks.exists() else None

    def location(self, obj):
        return obj.get_absolute_url()


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    protocol = 'http'  # ← http для локальной разработки

    def items(self):
        return ['home', 'catalog', 'about', 'contact', 'collections']

    def location(self, item):
        return reverse(item)