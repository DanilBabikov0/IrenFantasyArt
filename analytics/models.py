from django.db import models
from artworks.models import Artwork
from blog.models import BlogPost

class BlogPostView(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='views_log',
        verbose_name="Пост блога"
    )
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Время просмотра")

    class Meta:
        verbose_name = "Просмотр поста"
        verbose_name_plural = "Просмотры постов"
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['viewed_at']),
        ]

    def __str__(self):
        return f"{self.post.title} - {self.viewed_at}"
    
class ArtworkView(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='views_log',
        verbose_name="Картина"
    )
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Время просмотра")

    class Meta:
        verbose_name = "Просмотр"
        verbose_name_plural = "Просмотры"
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['viewed_at']),
        ]

    def __str__(self):
        return f"{self.artwork.title} - {self.viewed_at}"