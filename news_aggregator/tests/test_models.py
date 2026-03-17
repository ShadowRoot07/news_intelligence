from django.test import TestCase
from news_aggregator.models import Article

class ArticleModelTest(TestCase):
    def setUp(self):
        # Creamos un artículo de prueba
        self.article = Article.objects.create(
            title="Noticia de Prueba",
            url="https://test.com/noticia-1",
            source="Test Source",
            category="TEC"
        )

    def test_article_creation(self):
        """Verifica que el artículo se crea correctamente con sus valores base"""
        self.assertEqual(self.article.title, "Noticia de Prueba")
        self.assertEqual(self.article.category, "TEC")
        self.assertTrue(Article.objects.filter(url="https://test.com/noticia-1").exists())

