import os
import json
import time
import requests
from bs4 import BeautifulSoup
from groq import Groq
from .models import Article

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Configuración de fuentes (puedes añadir más URLs aquí)
SOURCES = [
    {'url': 'https://www.technologyreview.com/news/', 'cat': 'TEC', 'name': 'MIT Tech Review'},
    {'url': 'https://www.coindesk.com/', 'cat': 'CRP', 'name': 'CoinDesk'},
    {'url': 'https://www.reuters.com/business/healthcare-pharmaceuticals/', 'cat': 'MED', 'name': 'Reuters Health'},
    {'url': 'https://www.economist.com/finance-and-economics', 'cat': 'ECO', 'name': 'The Economist'},
    {'url': 'https://www.bbc.com/news/world', 'cat': 'POL', 'name': 'BBC World'},
]

def scrape_news():
    """Extrae titulares de las fuentes configuradas."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    total_added = 0

    for source in SOURCES:
        try:
            print(f"Buscando noticias en: {source['name']}...")
            response = requests.get(source['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos etiquetas de titulares comunes (h2, h3 o enlaces con texto)
            # Nota: Esto es genérico, algunos sitios pueden requerir selectores específicos
            headlines = soup.find_all(['h2', 'h3'], limit=5) 

            for h in headlines:
                title = h.get_text().strip()
                # Intentamos buscar un link cercano o el mismo tag si es <a>
                link_tag = h.find('a') if h.name != 'a' else h
                
                if title and len(title) > 10:
                    url_link = link_tag['href'] if link_tag and link_tag.has_attr('href') else source['url']
                    
                    # Asegurar URL absoluta
                    if url_link.startswith('/'):
                        from urllib.parse import urljoin
                        url_link = urljoin(source['url'], url_link)

                    obj, created = Article.objects.get_or_create(
                        url=url_link,
                        defaults={
                            'title': title,
                            'source': source['name'],
                            'category': source['cat']
                        }
                    )
                    if created:
                        total_added += 1

            print(f"Esperando 15 segundos para la próxima fuente...")
            time.sleep(15) # Retraso de cortesía solicitado

        except Exception as e:
            print(f"❌ Error scrapeando {source['name']}: {e}")
    
    return f"Se agregaron {total_added} titulares nuevos."

def analyze_with_groq():
    """Analiza con IA los artículos que no tienen resumen."""
    articles = Article.objects.filter(summary__isnull=True) | Article.objects.filter(summary="")
    count = 0

    for article in articles:
        try:
            cat_display = article.get_category_display()
            prompt = f"""
            Analiza esta noticia de la categoría {cat_display}:
            Título: "{article.title}"
            
            Debes proporcionar:
            1. Un resumen profesional de 2 párrafos sobre la noticia.
            2. Análisis de sentimiento: POSITIVO, NEGATIVO o NEUTRAL.
            3. Una explicación breve de por qué elegiste ese sentimiento.

            Responde ÚNICAMENTE en este formato JSON:
            {{
                "resumen": "texto del resumen",
                "sentimiento": "POSITIVO/NEGATIVO/NEUTRAL",
                "explicacion": "explicación breve"
            }}
            """

            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={ "type": "json_object" }
            )

            response_data = json.loads(completion.choices[0].message.content)

            article.summary = response_data.get("resumen")
            article.sentiment_label = response_data.get("sentimiento").capitalize()
            article.analysis_detail = response_data.get("explicacion")
            article.save()
            
            count += 1
            print(f"✅ Analizado por Groq: {article.title[:40]}...")
            
            # Un pequeño respiro también para la API de Groq
            time.sleep(2) 

        except Exception as e:
            print(f"❌ Error en Groq ID {article.id}: {e}")
            continue

    return f"Se procesaron {count} noticias con Groq."

def run_all():
    """Función maestra para ejecutar todo el flujo."""
    print(scrape_news())
    print(analyze_with_groq())

