import os
import json
import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from groq import Groq
from .models import Article

# Usamos una clave vacía si no existe para que no explote en local si no hay Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "no-key"))

SOURCES = [
    {'url': 'https://www.technologyreview.com/news/', 'cat': 'TEC', 'name': 'MIT Tech Review'},
    {'url': 'https://www.coindesk.com/', 'cat': 'CRP', 'name': 'CoinDesk'},
    {'url': 'https://www.reuters.com/business/healthcare-pharmaceuticals/', 'cat': 'MED', 'name': 'Reuters Health'},
    {'url': 'https://www.economist.com/finance-and-economics', 'cat': 'ECO', 'name': 'The Economist'},
    {'url': 'https://www.bbc.com/news/world', 'cat': 'POL', 'name': 'BBC World'},
]

def get_best_model():
    try:
        models_list = client.models.list()
        available_models = [m.id for m in models_list.data if "llama-3" in m.id.lower()]
        preferred = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192"]
        for p in preferred:
            if p in available_models:
                print(f"🤖 Modelo seleccionado: {p}")
                return p
        return available_models[0] if available_models else "llama-3.1-8b-instant"
    except Exception as e:
        print(f"⚠️ Error al listar modelos: {e}. Usando fallback.")
        return "llama-3.1-8b-instant"

def clean_url(url):
    return url.split('?')[0].split('#')[0].strip().rstrip('/')

def scrape_news():
    # User-Agent completo para evitar bloqueos de 403 Forbidden
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    total_added = 0

    for source in SOURCES:
        try:
            print(f"Scrapeando: {source['name']}...")
            response = requests.get(source['url'], headers=headers, timeout=20)
            
            # Debug para ver si el sitio nos deja entrar
            print(f"DEBUG: Status {response.status_code} de {source['name']}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos titulares en h2, h3 y también etiquetas 'a' que parecen titulares
            headlines = soup.find_all(['h2', 'h3'], limit=12)
            print(f"DEBUG: Encontrados {len(headlines)} candidatos en {source['name']}")

            for h in headlines:
                title = h.get_text().strip()
                
                # Buscamos el link: puede estar adentro, o el h2/h3 puede ser hijo de un <a>
                link_tag = h.find('a') 
                if not link_tag:
                    link_tag = h.find_parent('a')

                if title and len(title) > 15 and link_tag and link_tag.has_attr('href'):
                    full_url = urljoin(source['url'], link_tag['href'])
                    final_url = clean_url(full_url)

                    obj, created = Article.objects.get_or_create(
                        url=final_url,
                        defaults={
                            'title': title,
                            'source': source['name'],
                            'category': source['cat']
                        }
                    )
                    if created:
                        total_added += 1

            # Bajamos el sleep a 5 segundos para no agotar el tiempo de GitHub Actions
            time.sleep(5)
        except Exception as e:
            print(f"❌ Error en {source['name']}: {e}")

    return f">>> Éxito: {total_added} noticias nuevas."

def analyze_with_groq():
    # Buscamos artículos sin resumen
    articles = Article.objects.filter(summary__isnull=True) | Article.objects.filter(summary="")
    if not articles.exists():
        return ">>> No hay artículos para analizar."

    current_model = get_best_model()
    count = 0

    for article in articles:
        try:
            # Si no hay API KEY, saltamos (para evitar errores en local sin variables)
            if not os.environ.get("GROQ_API_KEY"):
                print("⚠️ Saltando análisis: GROQ_API_KEY no configurada.")
                break

            cat_display = article.get_category_display()
            prompt = f"""
            Analiza esta noticia de {cat_display}: "{article.title}"
            Genera un JSON con:
            1. "resumen": 2 párrafos profesionales en español.
            2. "sentimiento": POSITIVO, NEGATIVO o NEUTRAL.
            3. "explicacion": 1 frase del porqué.
            """

            completion = client.chat.completions.create(
                model=current_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            data = json.loads(completion.choices[0].message.content)
            article.summary = data.get("resumen", "Sin resumen.")
            article.sentiment_label = data.get("sentimiento", "Neutral").capitalize()
            article.analysis_detail = data.get("explicacion", "Sin detalle.")
            article.save()

            count += 1
            print(f"✅ Analizado: {article.title[:30]}...")
            time.sleep(1)

        except Exception as e:
            print(f"❌ Error Groq ID {article.id}: {e}")
            continue

    return f">>> IA: {count} artículos procesados con {current_model}."

def run_all():
    print(scrape_news())
    print(analyze_with_groq())

