from django.shortcuts import render
from .models import Article

def index(request):
    """Vista principal que muestra las últimas noticias analizadas."""
    # Traemos las noticias que ya tienen un resumen generado por la IA
    # Las ordenamos por fecha de publicación (la más reciente primero)
    articles = Article.objects.exclude(summary__isnull=True).exclude(summary="").order_by('-published_at')[:25]
    
    context = {
        'articles': articles,
        'title': 'Dashboard de Inteligencia'
    }
    return render(request, 'news_aggregator/index.html', context)

def category_view(request, cat_code):
    """Vista para filtrar noticias por categoría (TEC, CRP, etc)."""
    articles = Article.objects.filter(category=cat_code).exclude(summary="").order_by('-published_at')
    
    # Obtenemos el nombre amigable de la categoría desde el modelo
    cat_name = dict(Article.CATEGORIES).get(cat_code, cat_code)
    
    context = {
        'articles': articles,
        'title': f'Noticias: {cat_name}'
    }
    return render(request, 'news_aggregator/index.html', context)

