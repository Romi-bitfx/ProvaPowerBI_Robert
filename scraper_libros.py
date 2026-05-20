import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extraer_libros():
    print("🚀 [CI/CD] Iniciando Extractor de Libros...")
    url = "http://books.toscrape.com/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"📡 Conectando con {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Conexión exitosa. Analizando el catálogo...")
            soup = BeautifulSoup(response.text, 'html.parser')
            libros = soup.select('article.product_pod')
            
            # 📝 Abrimos (o creamos) el archivo libros.txt para escribir el resultado
            with open("libros.txt", "w", encoding="utf-8") as f:
                # Escribimos el encabezado tanto en consola como en el archivo
                fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
                encabezado = f"📚 CATÁLOGO DE LIBROS Y PRECIOS ({fecha_actual})\n" + "=" * 60 + "\n"
                
                print(encabezado)
                f.write(encabezado)
                
                for i, libro in enumerate(libros[:15], 1):
                    titulo = libro.select_one('h3 a')['title']
                    precio = libro.select_one('p.price_color').text
                    
                    linea_libro = f"{i}. 📖 {titulo}\n   💰 Precio: {precio}\n\n"
                    
                    print(linea_libro) # Se ve en los logs de GitHub
                    f.write(linea_libro) # Se guarda en el archivo txt
                    
                f.write("=" * 60 + "\n")
            
            print("💾 Archivo 'libros.txt' generado correctamente en el servidor.")
            
        else:
            print(f"❌ Error al acceder a la web. Código de estado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ocurrió un error durante el scraping: {e}")

if __name__ == "__main__":
    extraer_libros()
