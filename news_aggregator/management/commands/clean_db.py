from django.core.management.base import BaseCommand
from news_aggregator.models import Article

class Command(BaseCommand):
    help = 'Borra todos los artículos de la base de datos de Neon'

    def handle(self, *args, **options):
        count = Article.objects.count()
        if count == 0:
            self.stdout.write(self.style.WARNING("La base de datos ya está vacía."))
            return

        self.stdout.write(f"Borrando {count} artículos...")
        Article.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✅ Base de datos limpiada con éxito."))

