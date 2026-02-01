# blog/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import re
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from unidecode import unidecode
import os


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
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['status', '-views']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['slug']),
            models.Index(fields=['tags']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Флаг для отслеживания, было ли изображение сжато
        is_new_image = False
        
        # Сжимаем изображение только при первой загрузке или изменении
        if self.preview_image and not self.pk:
            is_new_image = True
        elif self.preview_image and self.pk:
            # Проверяем, изменилось ли изображение
            try:
                old_instance = BlogPost.objects.get(pk=self.pk)
                if old_instance.preview_image != self.preview_image:
                    is_new_image = True
            except BlogPost.DoesNotExist:
                is_new_image = True
        
        # Сжимаем и транслитерируем только новые или изменённые изображения
        if is_new_image and self.preview_image:
            try:
                img = Image.open(self.preview_image)
                
                # Максимальные размеры для превью
                max_width = 1200
                max_height = 800
                
                # Изменяем размер если нужно
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Конвертируем в RGB если нужно
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                
                # Сохраняем в буфер
                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=85, optimize=True)
                img_io.seek(0)
                
                # Транслитерируем имя файла
                original_name = os.path.basename(self.preview_image.name)
                name, ext = os.path.splitext(original_name)
                
                # Конвертируем кириллицу в латиницу
                name = unidecode(name)  # Транслитерация
                name = slugify(name)     # Убираем спецсимволы, делаем нижний регистр
                
                new_name = f"{name}_preview.jpg"
                
                self.preview_image.save(
                    new_name,
                    ContentFile(img_io.getvalue()),
                    save=False
                )
            except Exception as e:
                # Если ошибка при сжатии, оставляем оригинальное изображение
                print(f"Ошибка сжатия превью изображения: {e}")
        
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