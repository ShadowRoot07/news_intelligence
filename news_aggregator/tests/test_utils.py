from django.test import TestCase
from unittest.mock import patch, MagicMock
from news_aggregator.utils import scrape_news, clean_url

class UtilsTest(TestCase):

    def test_clean_url(self):
        """Verifica que la limpieza de URLs elimine parámetros y fragmentos"""
        url_sucia = "https://ejemplo.com/noticia/?utm_source=tracker#seccion"
        url_limpia = clean_url(url_sucia)
        self.assertEqual(url_limpia, "https://ejemplo.com/noticia")

    @patch('news_aggregator.utils.requests.get')
    def test_scrape_news_mock(self, mock_get):
        """Simula un scrapeo exitoso sin hacer peticiones reales a internet"""
        # Configuramos un HTML falso que el mock devolverá
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <body>
                    <h2><a href="/cyber-attack">Ataque masivo detectado</a></h2>
                </body>
            </html>
        """
        mock_get.return_value = mock_response

        # Ejecutamos el scraper (solo para una fuente para ir rápido)
        # Usamos patch para SOURCES si quisiéramos limitar el bucle, 
        # pero aquí veremos si al menos procesa un h2
        from news_aggregator.models import Article
        from news_aggregator import utils
        
        # Simulamos que solo hay una fuente para el test
        with patch('news_aggregator.utils.SOURCES', [{'url': 'https://test.com', 'cat': 'CYB', 'name': 'Test'}]):
            resultado = scrape_news()
            self.assertIn("Éxito: 1 noticias nuevas", resultado)
            self.assertTrue(Article.objects.filter(title="Ataque masivo detectado").exists())

