from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDay

from artworks.models import Artwork, Theme
from blog.models import BlogPost
from .models import ArtworkView, BlogPostView  # исправленный импорт


@staff_member_required
def analytics_dashboard(request):
    # --- Данные для картин ---
    top_artworks = Artwork.objects.filter(views__gt=0).order_by('-views')[:10]

    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    artwork_daily_views = (
        ArtworkView.objects
        .filter(viewed_at__gte=start_date)
        .annotate(day=TruncDay('viewed_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    artwork_chart_labels = [item['day'].strftime('%d.%m') for item in artwork_daily_views]
    artwork_chart_data = [item['count'] for item in artwork_daily_views]

    themes = Theme.objects.all()
    theme_data = []
    for theme in themes:
        total_views = Artwork.objects.filter(theme=theme).aggregate(total=Sum('views'))['total'] or 0
        if total_views > 0:
            theme_data.append({'name': theme.name, 'views': total_views})
    theme_data.sort(key=lambda x: x['views'], reverse=True)
    top_themes = theme_data[:5]

    # --- Данные для блога ---
    top_posts = BlogPost.objects.filter(status='published', views__gt=0).order_by('-views')[:10]

    blog_daily_views = (
        BlogPostView.objects
        .filter(viewed_at__gte=start_date)
        .annotate(day=TruncDay('viewed_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    blog_chart_labels = [item['day'].strftime('%d.%m') for item in blog_daily_views]
    blog_chart_data = [item['count'] for item in blog_daily_views]

    posts = BlogPost.objects.filter(status='published', tags__isnull=False).exclude(tags='')
    tag_views = {}
    for post in posts:
        tags_list = post.get_tags_list()
        for tag in tags_list:
            tag_views[tag] = tag_views.get(tag, 0) + post.views
    sorted_tags = sorted(tag_views.items(), key=lambda x: x[1], reverse=True)[:10]
    top_tags = [{'name': tag, 'views': views} for tag, views in sorted_tags]

    context = {
        'top_artworks': top_artworks,
        'artwork_chart_labels': artwork_chart_labels,
        'artwork_chart_data': artwork_chart_data,
        'top_themes': top_themes,
        'top_posts': top_posts,
        'blog_chart_labels': blog_chart_labels,
        'blog_chart_data': blog_chart_data,
        'top_tags': top_tags,
    }
    return render(request, 'analytics/dashboard.html', context)