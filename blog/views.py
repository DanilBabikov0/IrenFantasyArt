# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.db.models.functions import Lower
from .models import BlogPost
from collections import Counter
import re

def blog_list(request):
    """Список постов блога"""
    
    # Кэширование популярных и недавних постов (опционально)
    cache_key_popular = 'blog_popular_posts'
    cache_key_recent = 'blog_recent_posts'
    
    # Основной запрос с оптимизацией
    posts = BlogPost.objects.filter(status='published').select_related('author')
    
    # Поиск
    query = request.GET.get('q', '').strip()
    if query:
        # Оптимизированный поиск - сначала по заголовку и тегам, потом по контенту
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query) |
            Q(excerpt__icontains=query)
        )
        # Поиск по контенту только если не нашли по другим полям
        if not posts.exists():
            posts = BlogPost.objects.filter(status='published').filter(
                content__icontains=query
            ).select_related('author')
    
    # Фильтр по тегу
    tag = request.GET.get('tag', '').strip()
    if tag:
        posts = posts.filter(tags__icontains=tag)
    
    # Сортировка
    posts = posts.order_by('-published_at')
    
    # Пагинация
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
    
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)
    
    # Получаем топ теги (оптимизированно)
    top_tags = []
    all_posts_with_tags = BlogPost.objects.filter(
        status='published'
    ).values_list('tags', flat=True)
    
    # Собираем все теги
    all_tags = []
    for tags_str in all_posts_with_tags:
        if tags_str:
            tags_list = [t.strip() for t in tags_str.split(',')]
            all_tags.extend(tags_list)
    
    # Считаем топ-10 тегов
    tag_counter = Counter(all_tags)
    top_tags = tag_counter.most_common(10)
    
    # Получаем популярные посты (оптимизированно)
    popular_posts = BlogPost.objects.filter(
        status='published'
    ).select_related('author').order_by('-views')[:5]
    
    # Получаем недавние посты (оптимизированно)
    recent_posts = BlogPost.objects.filter(
        status='published'
    ).select_related('author').order_by('-published_at')[:5]
    
    context = {
        'posts': posts_page,
        'query': query,
        'tag': tag,
        'is_paginated': posts_page.has_other_pages(),
        'page_obj': posts_page,
        'top_tags': top_tags,
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """Детальная страница поста"""
    # Оптимизированный запрос
    post = get_object_or_404(
        BlogPost.objects.select_related('author'),
        slug=slug,
        status='published'
    )
    
    # Отслеживание просмотров (оптимизированно)
    viewed_posts = request.session.get('viewed_posts', [])
    
    if post.id not in viewed_posts:
        # Используем F-выражение для атомарного обновления
        from django.db.models import F
        BlogPost.objects.filter(id=post.id).update(views=F('views') + 1)
        post.views += 1  # Обновляем локально для отображения
        viewed_posts.append(post.id)
        if len(viewed_posts) > 50:
            viewed_posts = viewed_posts[-50:]
        request.session['viewed_posts'] = viewed_posts
    
    # Похожие посты (оптимизированно)
    similar_posts = BlogPost.objects.filter(
        status='published'
    ).exclude(id=post.id).select_related('author')
    
    tags = post.get_tags_list()
    
    if tags:
        # Используем Q-объекты для поиска по тегам
        q_objects = Q()
        for tag in tags:
            q_objects |= Q(tags__icontains=tag)
        similar_posts = similar_posts.filter(q_objects)[:4]
    else:
        # Случайный выбор без тегов
        similar_posts = similar_posts.order_by('?')[:4]
    
    context = {
        'post': post,
        'similar_posts': similar_posts,
    }
    
    return render(request, 'blog/blog_detail.html', context)