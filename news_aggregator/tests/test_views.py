from django.test import TestCase
from django.urls import reverse

class NewsViewsTest(TestCase):
    def test_index_view_status_code(self):
        """Verifica que la home de Shadow News AI responde correctamente"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_category_view_status_code(self):
        """Verifica que la categoría de Ciberseguridad funciona"""
        response = self.client.get(reverse('category', args=['CYB']))
        self.assertEqual(response.status_code, 200)

