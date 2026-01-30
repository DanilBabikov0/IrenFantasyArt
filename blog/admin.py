# blog/admin.py
from django.contrib import admin
from django import forms
from .models import BlogPost
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = BlogPost
        fields = '__all__'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'author', 'status', 'published_at', 'views', 'created_at')
    list_filter = ('status', 'author', 'published_at')
    search_fields = ('title', 'tags', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
    
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'author', 'preview_image', 'excerpt')
        }),
        ('Содержимое', {
            'fields': ('content', 'tags')
        }),
        ('Статус и даты', {
            'fields': ('status', 'published_at')
        }),
        ('Статистика', {
            'fields': ('views',)
        }),
    )

    readonly_fields = ['views']
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)