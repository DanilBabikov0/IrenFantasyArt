# artworks/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Theme, Collection, Artwork, ArtworkImage
from django.core.exceptions import SuspiciousFileOperation


class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 3
    fields = ['image', 'order', 'is_primary']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('order')

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'theme', 'status', 'price', 'views', 'created_year']
    list_filter = ['category', 'theme', 'collection', 'status', 'created_year']
    search_fields = ['title', 'short_description', 'tags', 'description']
    list_editable = ['status', 'price']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArtworkImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'theme', 'collection', 'tags')
        }),
        ('Продажа и статус', {
            'fields': ('status', 'price', 'purchase_url')
        }),
        ('Технические данные', {
            'fields': ('width_cm', 'height_cm', 'created_year')
        }),
        ('Описания', {
            'fields': ('short_description', 'description')
        }),
        ('Статистика', {
            'fields': ('views', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['views', 'created_at', 'updated_at']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'artworks_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def artworks_count(self, obj):
        return obj.artwork_set.count()
    artworks_count.short_description = 'Количество работ'

@admin.register(ArtworkImage)
class ArtworkImageAdmin(admin.ModelAdmin):
    list_display = ['artwork', 'image_preview', 'order', 'is_primary']
    list_filter = ['artwork__category', 'is_primary']
    list_editable = ['order', 'is_primary']
    search_fields = ['artwork__title']
    
    def image_preview(self, obj):
        if obj.image:
            try:
                return format_html(
                    '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                    obj.image.url
                )
            except (ValueError, SuspiciousFileOperation):
                return format_html('<span style="color: red;">Ошибка пути</span>')
        return "-"
    image_preview.short_description = 'Превью'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Collection, CollectionAdmin)