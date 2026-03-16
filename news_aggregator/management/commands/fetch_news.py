from django.core.management.base import BaseCommand
from news_aggregator.utils import run_all

class Command(BaseCommand):
    help = 'Ejecuta el scraper y el análisis de IA para nuevas noticias'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Iniciando Shadow News Scraper ---"))
        try:
            run_all()
            self.stdout.write(self.style.SUCCESS("--- Proceso completado exitosamente ---"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante la ejecución: {e}"))

