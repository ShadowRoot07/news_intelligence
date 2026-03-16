from django.shortcuts import render
from .models import Article

def index(request):
    """Muestra las noticias más recientes primero."""
    articles = Article.objects.exclude(summary__isnull=True).exclude(summary="").order_by('-published_at')[:30]
    
    context = {
        'articles': articles,
        'title': 'Dashboard de Inteligencia'
    }
    return render(request, 'news_aggregator/index.html', context)

def category_view(request, cat_code):
    """Filtrado por categoría con orden cronológico."""
    articles = Article.objects.filter(category=cat_code).exclude(summary="").order_by('-published_at')
    cat_name = dict(Article.CATEGORIES).get(cat_code, cat_code)

    context = {
        'articles': articles,
        'title': f'Noticias: {cat_name}'
    }
    return render(request, 'news_aggregator/index.html', context)

