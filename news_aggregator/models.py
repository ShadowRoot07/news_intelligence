from django.db import models

class Article(models.Model):
    CATEGORIES = [
        ('MED', 'Medicina'),
        ('POL', 'Política'),
        ('TEC', 'Tecnología'),
        ('ECO', 'Economía'),
        ('CRP', 'Criptomonedas'),
        ('CYB', 'Ciberseguridad'),  # <-- Nueva categoría
    ]

    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    source = models.CharField(max_length=100)
    category = models.CharField(max_length=3, choices=CATEGORIES, default='TEC')
    summary = models.TextField(blank=True, null=True)
    sentiment_label = models.CharField(max_length=20, default="Neutral")
    analysis_detail = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.category}] {self.title}"

