# artworks/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.functional import cached_property
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    

class Theme(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название тематики")
    
    class Meta:
        verbose_name = "Тематика"
        verbose_name_plural = "Тематики"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название коллекции")
    slug = models.SlugField(max_length=100, unique=True, blank=False)
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to='collections/', 
        blank=True, 
        null=True,
        verbose_name="Обложка коллекции"
    )
    
    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @cached_property
    def artwork_count(self):
        """Количество работ в коллекции"""
        return self.artwork_set.count()
    
    def get_absolute_url(self):
        return reverse('collection_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Artwork(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=False, verbose_name="URL поста")

    tags = models.CharField(
        max_length=500, 
        blank=True,
        verbose_name="Теги",
        help_text="Перечислите через запятую: например, пейзаж, море, лето"
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория"
    )
    theme = models.ForeignKey(
        Theme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Тематика"
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Коллекция"
    )
  
    STATUS_CHOICES = [
        ('available', 'В наличии'),
        ('sold', 'Нет в наличии'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='available',
        verbose_name="Статус"
    )
    
    price = models.PositiveIntegerField(
        verbose_name="Цена (руб)",
        null=True,
        blank=True,
        help_text="Оставьте пустым для 'Цена по запросу'"
    )
    purchase_url = models.URLField(
        verbose_name="Ссылка для покупки", 
        blank=True,
        help_text="Ссылка на внешний магазин или форма запроса, по умалчанию ссылка на контакты"
    )
    
    SIZE_CHOICES = [
        ('small', 'Маленькие (до 25×25)'),
        ('medium', 'Средние (до 40×60)'),
        ('large', 'Большие (свыше 40×60 см)'),
    ]
    width_cm = models.PositiveIntegerField(
        verbose_name="Ширина (см)",
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )
    height_cm = models.PositiveIntegerField(
        verbose_name="Высота (см)",
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )
    
    @property
    def size_category(self):
        w, h = self.width_cm, self.height_cm
        if w <= 25 and h <= 25:
            return 'small'
        elif (w <= 40 and h <= 60) or (w <= 60 and h <= 40):
            return 'medium'
        else:
            return 'large'
    
    created_year = models.PositiveIntegerField(
        verbose_name="Год создания",
        validators=[MinValueValidator(1900), MaxValueValidator(2200)]
    )
    
    short_description = models.TextField(
        max_length=300, 
        verbose_name="Краткое описание",
        help_text="Для превью в каталоге"
    )
    description = models.TextField(verbose_name="Полное описание")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    
    class Meta:
        verbose_name = "Картина"
        verbose_name_plural = "Картины"
        ordering = ['-created_year', '-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['theme']),
            models.Index(fields=['collection']),
            models.Index(fields=['created_year']),
            models.Index(fields=['price']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Artwork.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('artwork_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def get_price_display(self):
        if self.status == 'sold':
            return "Нет в наличии"
        if self.price:
            return f"{self.price:,.0f} руб.".replace(',', ' ')
        return "Цена по запросу"
    
    def get_dimensions(self):
        return f"{self.width_cm}×{self.height_cm} см"
    
    def get_size_category_display(self):
        size_map = {
            'small': 'Маленькие',
            'medium': 'Средние',
            'large': 'Большие'
        }
        return size_map.get(self.size_category, 'Неизвестно')
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def __str__(self):
        return f"{self.title} ({self.created_year})"


class ArtworkImage(models.Model):
    artwork = models.ForeignKey(
        Artwork, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='artworks/%Y/%m/%d/')
    order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order', 'id']
    
    def save(self, *args, **kwargs):
        if not self.pk and not ArtworkImage.objects.filter(artwork=self.artwork).exists():
            self.is_primary = True
        
        if self.is_primary:
            ArtworkImage.objects.filter(
                artwork=self.artwork, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Изображение для {self.artwork.title}"