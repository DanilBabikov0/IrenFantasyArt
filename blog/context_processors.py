# blog/context_processors.py
from .models import BlogPost
from collections import Counter

def blog_context(request):
    popular_posts = BlogPost.objects.filter(status='published').order_by('-views')[:5]
    recent_posts = BlogPost.objects.filter(status='published').order_by('-published_at')[:5]
    
    all_tags = []
    for post in BlogPost.objects.filter(status='published'):
        all_tags.extend(post.get_tags_list())
    
    tag_counts = Counter(all_tags)
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
        'top_tags': top_tags,
    }