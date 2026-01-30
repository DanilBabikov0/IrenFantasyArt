# blog/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import re
from django.utils import timezone


class BlogPost(models.Model):
    POST_STATUS = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('archived', 'В архиве'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL поста")
    
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Автор",
        related_name='blog_posts'
    )
    
    tags = models.CharField(
        max_length=500, 
        blank=True,
        verbose_name="Теги",
        help_text="Перечислите теги через запятую"
    )
    
    content = RichTextUploadingField(
        verbose_name="Содержимое",
        config_name='default'
    )
    
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    
    status = models.CharField(
        max_length=20, 
        choices=POST_STATUS, 
        default='draft',
        verbose_name="Статус"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата публикации")
    
    preview_image = models.ImageField(
        upload_to='blog/previews/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name="Превью изображение",
        help_text="Изображение для превью в списке постов"
    )
    
    excerpt = models.TextField(
        max_length=500, 
        blank=True,
        verbose_name="Краткое описание",
        help_text="Если оставить пустым, будет сгенерировано автоматически"
    )
    
    class Meta:
        verbose_name = "Пост блога"
        verbose_name_plural = "Посты блога"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        if not self.excerpt and self.content:
            from django.utils.html import strip_tags
            plain_text = strip_tags(self.content)[:500]
            if len(plain_text) > 497:
                plain_text = plain_text[:plain_text.rfind(' ')]
            self.excerpt = plain_text + '...'
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        """Возвращает список тегов"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_content_html(self):
        return self.content