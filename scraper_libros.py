import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extraer_libros():
    print("🚀 [CI/CD] Iniciando Extractor de Libros...")
    
    # Esta web está diseñada para hacer pruebas de scraping, no nos bloqueará
    url = "http://books.toscrape.com/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"📡 Conectando con {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Conexión exitosa. Analizando el catálogo...\n")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cada libro está dentro de una etiqueta <article> con la clase "product_pod"
            libros = soup.select('article.product_pod')
            
            print(f"📚 CATÁLOGO DE LIBROS Y PRECIOS ({datetime.now().strftime('%d/%m/%Y %H:%M')})")
            print("=" * 60)
            
            if not libros:
                print("⚠️ No se encontraron libros en la página.")
            
            # Recorremos los libros encontrados (limitamos a 15 para la consola)
            for i, libro in enumerate(libros[:15], 1):
                # El título completo suele estar en el atributo 'title' del enlace (<a>) dentro del <h3>
                titulo = libro.select_one('h3 a')['title']
                
                # El precio está en un párrafo (<p>) con la clase 'price_color'
                precio = libro.select_one('p.price_color').text
                
                print(f"{i}. 📖 {titulo} ")
                print(f"   💰 Precio: {precio}\n")
                
            print("=" * 60)
            
        else:
            print(f"❌ Error al acceder a la web. Código de estado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ocurrió un error durante el scraping: {e}")

if __name__ == "__main__":
    extraer_libros()
