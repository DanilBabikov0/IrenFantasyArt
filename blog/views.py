# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import BlogPost


def blog_list(request):
    """Список постов блога"""
    posts = BlogPost.objects.filter(status='published')
    
    # Поиск
    query = request.GET.get('q', '').strip()
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        ).distinct()
    
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
    
    context = {
        'posts': posts_page,
        'query': query,
        'tag': tag,
        'is_paginated': posts_page.has_other_pages(),
        'page_obj': posts_page,
    }
    
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """Детальная страница поста"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    viewed_posts = request.session.get('viewed_posts', [])
    
    if post.id not in viewed_posts:
        post.increment_views()
        viewed_posts.append(post.id)
        if len(viewed_posts) > 50:
            viewed_posts = viewed_posts[-50:]
        request.session['viewed_posts'] = viewed_posts
    
    similar_posts = BlogPost.objects.filter(status='published').exclude(id=post.id)
    tags = post.get_tags_list()
    
    if tags:
        q_objects = Q()
        for tag in tags:
            q_objects |= Q(tags__icontains=tag)
        similar_posts = similar_posts.filter(q_objects).distinct()[:4]
    else:
        similar_posts = similar_posts.order_by('?')[:4]
    
    context = {
        'post': post,
        'similar_posts': similar_posts,
    }
    
    return render(request, 'blog/blog_detail.html', context)