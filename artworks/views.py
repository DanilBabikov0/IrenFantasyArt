# artworks/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Artwork, Category, Theme, Collection, ArtworkImage
from .filters import ArtworkFilter
import random


def catalog(request):
    """Каталог с фильтрами, поиском и пагинацией"""
    artworks_qs = Artwork.objects.all().select_related(
        'category', 'theme'
    ).prefetch_related('images')
    
    query = request.GET.get('q', '').strip()
    if query:
        artworks_qs = artworks_qs.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        )
    
    artwork_filter = ArtworkFilter(request.GET, queryset=artworks_qs)
    filtered_artworks = artwork_filter.qs
    
    order_by = request.GET.get('order', '-created_at')
    
    valid_orders = [
        '-created_at', 'created_at', 
        'price', '-price', 
        '-views', 
        '-created_year', 'created_year',
        'title', '-title'
    ]
    if order_by in valid_orders:
        filtered_artworks = filtered_artworks.order_by(order_by)
    else:
        order_by = '-created_at'
        filtered_artworks = filtered_artworks.order_by(order_by)
    
    per_page = request.GET.get('per_page', '12')
    try:
        per_page = int(per_page)
        if per_page not in [12, 24, 48]:
            per_page = 12
    except (ValueError, TypeError):
        per_page = 12
    
    paginator = Paginator(filtered_artworks, per_page)
    page = request.GET.get('page', 1)
    
    try:
        artworks = paginator.page(page)
    except PageNotAnInteger:
        artworks = paginator.page(1)
    except EmptyPage:
        artworks = paginator.page(paginator.num_pages)
    
    # Получаем все категории, тематики, коллекции для фильтров
    all_categories = Category.objects.all()
    all_themes = Theme.objects.all()
    
    # Получаем выбранные значения для чекбоксов
    selected_categories = request.GET.getlist('category')
    selected_themes = request.GET.getlist('theme')
    selected_sizes = request.GET.getlist('size')
    selected_statuses = request.GET.getlist('status')
    
    show_available_only = 'available' in selected_statuses and len(selected_statuses) == 1
    
    status_choices = Artwork.STATUS_CHOICES
    
    # SEO-заголовок
    seo_title = "Каталог картин | IrenFantasyArt"
    if query:
        seo_title = f"Поиск: '{query}' | Каталог картин | IrenFantasyArt"
    
    context = {
        'artworks': artworks,
        'current_order': order_by,
        'filter': artwork_filter,
        'all_categories': all_categories,
        'all_themes': all_themes,
        'query': query,
        'total_count': artworks_qs.count(),
        'filtered_count': filtered_artworks.count(),
        'seo_title': seo_title,
        'selected_categories': selected_categories,
        'selected_themes': selected_themes,
        'selected_sizes': selected_sizes,
        'selected_statuses': selected_statuses,
        'status_choices': status_choices,
        'show_available_only': show_available_only,
        'per_page': per_page,
        'page': page,
        'current_order': order_by,
        'request': request,
    }
    
    return render(request, 'artworks/catalog.html', context)


def artwork_detail(request, slug):
    """Детальная страница картины"""
    artwork = get_object_or_404(
        Artwork.objects.select_related('category', 'theme', 'collection')
                       .prefetch_related('images'),
        slug=slug
    )

    viewed_artworks = request.session.get('viewed_artworks', [])
    
    if artwork.id not in viewed_artworks:
        artwork.increment_views()
        viewed_artworks.append(artwork.id)
        if len(viewed_artworks) > 50:
            viewed_artworks = viewed_artworks[-50:]
        request.session['viewed_artworks'] = viewed_artworks
    
    similar_artworks = Artwork.objects.filter(
        status='available'
    ).exclude(
        id=artwork.id
    ).select_related('category', 'theme').prefetch_related('images')
    
    if artwork.theme:
        similar_artworks = similar_artworks.filter(theme=artwork.theme)
    elif artwork.category:
        similar_artworks = similar_artworks.filter(category=artwork.category)
    
    similar_artworks = similar_artworks[:4]
    
    collection_artworks = None
    if artwork.collection:
        collection_artworks = Artwork.objects.filter(
            collection=artwork.collection,
            status='available'
        ).exclude(
            id=artwork.id
        ).select_related('category', 'theme').prefetch_related('images')[:4]
    
    context = {
        'artwork': artwork,
        'similar_artworks': similar_artworks,
        'collection_artworks': collection_artworks,
    }
    
    return render(request, 'artworks/detail.html', context)


def collections_list(request):
    """Страница со списком всех коллекций"""
    collections = Collection.objects.annotate(
        artwork_count=Count('artwork')
    ).order_by('name')
    
    collections_with_images = collections.exclude(
        Q(image='') | Q(image__isnull=True)
    )[:10]
    
    total_artworks = Artwork.objects.filter(collection__isnull=False).count()

    available_artworks = Artwork.objects.filter(
        status='available',
        collection__isnull=False
    ).count()
    
    context = {
        'collections': collections,
        'collections_with_images': collections_with_images,
        'total_artworks': total_artworks,
        'available_artworks': available_artworks,
    }
    
    return render(request, 'artworks/collections.html', context)


def collection_detail(request, slug):
    """Детальная страница коллекции"""
    collection = get_object_or_404(Collection, slug=slug)
    
    artworks_qs = Artwork.objects.filter(
        collection=collection
    ).select_related('category', 'theme').prefetch_related('images')
    
    carousel_images = []
    for artwork in artworks_qs.filter(images__isnull=False)[:10]:
        if artwork.images.exists():
            first_image = artwork.images.first()
            if first_image:
                carousel_images.append({
                    'url': first_image.image.url,
                    'alt': artwork.title,
                    'artwork_url': artwork.get_absolute_url()
                })
    
    if not carousel_images and collection.image:
        carousel_images.append({
            'url': collection.image.url,
            'alt': collection.name,
            'artwork_url': None
        })
    
    available_count = artworks_qs.filter(status='available').count()
    sold_count = artworks_qs.filter(status='sold').count()
    
    paginator = Paginator(artworks_qs, 12)
    page = request.GET.get('page', 1)
    
    try:
        artworks = paginator.page(page)
    except PageNotAnInteger:
        artworks = paginator.page(1)
    except EmptyPage:
        artworks = paginator.page(paginator.num_pages)
    
    other_collections = Collection.objects.exclude(
        id=collection.id
    )[:6]
    
    context = {
        'collection': collection,
        'artworks': artworks,
        'carousel_images': carousel_images,
        'available_count': available_count,
        'sold_count': sold_count,
        'other_collections': other_collections,
    }
    
    return render(request, 'artworks/collection.html', context)


def home(request):
    """Главная страница"""
    # Лучшие работы для слайдера (3 самые популярные)
    featured_artworks = Artwork.objects.filter(
        status='available'
    ).order_by('-views')[:3]
    
    # Одна случайная картина маслом (ID категории 1)
    oil_artworks = Artwork.objects.filter(
        status='available',
        category_id=1
    )
    oil_artwork = random.choice(list(oil_artworks)) if oil_artworks.exists() else None
    
    # Одна случайная картина пастелью (ID категории 2)
    pastel_artworks = Artwork.objects.filter(
        status='available',
        category_id=2
    )
    pastel_artwork = random.choice(list(pastel_artworks)) if pastel_artworks.exists() else None
    
    # Одна случайная маленькая картина
    small_artworks = Artwork.objects.filter(
        status='available',
        width_cm__lte=25,
        height_cm__lte=25
    )
    small_artwork = random.choice(list(small_artworks)) if small_artworks.exists() else None
    
    # Одна случайная большая картина
    large_artworks = Artwork.objects.filter(
        status='available'
    ).filter(
        Q(width_cm__gt=40) | Q(height_cm__gt=60)
    )
    large_artwork = random.choice(list(large_artworks)) if large_artworks.exists() else None
    
    # 4 последних поста из блога
    recent_posts = []
    try:
        from blog.models import BlogPost
        recent_posts = BlogPost.objects.filter(
            status='published'
        ).order_by('-created_at')[:4]
    except (ImportError, RuntimeError):
        # Если блог не установлен
        pass
    
    context = {
        'featured_artworks': featured_artworks,
        'oil_artwork': oil_artwork,
        'pastel_artwork': pastel_artwork,
        'small_artwork': small_artwork,
        'large_artwork': large_artwork,
        'recent_posts': recent_posts,
    }
    return render(request, 'artworks/home.html', context)

def about(request):
    """Страница 'Обо мне'"""
    # Получаем 12 самых популярных картин (по просмотрам)
    popular_artworks = Artwork.objects.filter(
        status='available'
    ).order_by('-views')[:12]
    
    context = {
        'popular_artworks': popular_artworks,
    }
    return render(request, 'artworks/about.html', context)


def contact(request):
    """Страница 'Контакты'"""
    # Получаем 12 самых популярных картин
    popular_artworks = Artwork.objects.filter(
        status='available'
    ).order_by('-views')[:12]
    
    # Получаем 12 популярных постов из блога
    popular_posts = []
    try:
        from blog.models import BlogPost
        popular_posts = BlogPost.objects.filter(
            status='published'
        ).order_by('-views')[:12]
    except (ImportError, RuntimeError):
        pass
    
    context = {
        'popular_artworks': popular_artworks,
        'popular_posts': popular_posts,
    }
    return render(request, 'artworks/contact.html', context)


def terms(request):
    """Страница 'Условия покупки и доставки'"""
    return render(request, 'artworks/terms.html')


def search(request):
    """Глобальный поиск по сайту"""
    query = request.GET.get('q', '').strip()
    results = {
        'artworks': [],
        'collections': [],
        'posts': [],
    }
    
    total_artworks = Artwork.objects.count()
    total_collections = Collection.objects.count()
    
    try:
        from blog.models import BlogPost
        total_posts = BlogPost.objects.filter(status='published').count()
    except (ImportError, RuntimeError):
        total_posts = 0
    
    if query:
        # Поиск по картинам
        results['artworks'] = Artwork.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(tags__icontains=query)
        ).select_related('category', 'theme', 'collection').prefetch_related('images')[:20]
        
        # Поиск по коллекциям
        results['collections'] = Collection.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:10]
        
        # Поиск по постам блога
        try:
            from blog.models import BlogPost
            results['posts'] = BlogPost.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(tags__icontains=query),
                status='published'
            ).select_related('author')[:10]
        except (ImportError, RuntimeError):
            results['posts'] = []
    
    context = {
        'query': query,
        'results': results,
        'artworks_count': len(results['artworks']),
        'collections_count': len(results['collections']),
        'posts_count': len(results['posts']),
        'total_artworks': total_artworks,
        'total_collections': total_collections,
        'total_posts': total_posts,
    }
    
    return render(request, 'artworks/search.html', context)