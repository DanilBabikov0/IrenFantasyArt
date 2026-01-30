from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path 
from django.contrib.sitemaps.views import sitemap
from artworks.sitemaps import ArtworkSitemap, CollectionSitemap, StaticViewSitemap
from blog.sitemaps import BlogPostSitemap, BlogStaticSitemap
from django.views.generic import TemplateView

sitemaps = {
    'artworks': ArtworkSitemap,
    'collections': CollectionSitemap,
    'blog_posts': BlogPostSitemap,
    'static': StaticViewSitemap,
    'blog_static': BlogStaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('artworks.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, 
         name='django.contrib.sitemaps.views.sitemap'),
    
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    ), name='robots_txt'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]