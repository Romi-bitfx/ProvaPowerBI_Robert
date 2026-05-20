import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extraer_dispositivos_apple():
    print("🚀 [CI/CD] Iniciando Extractor de Dispositivos Apple...")
    
    # Usamos la página de iPhone de Apple España como ejemplo
    url = "https://www.apple.com/es/iphone/"
    
    # Es VITAL usar un User-Agent muy realista, ya que Apple bloquea inmediatamente peticiones sospechosas
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    try:
        print(f"📡 Conectando con {url}...")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print("✅ Conexión exitosa. Analizando la estructura de Apple...")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Apple suele estructurar sus productos usando etiquetas h3 con clases específicas de tipografía
            # O selectores como los nombres de los modelos en sus tarjetas de comparación
            productos = soup.select('h3.typography-product-headline, .typography-family-headline, h3.card-headline')
            
            print(f"\n🍏 DISPOSITIVOS LOCALIZADOS ({datetime.now().strftime('%d/%m/%Y %H:%M')})")
            print("=" * 60)
            
            contador = 0
            for p in productos:
                nombre = p.get_text().strip()
                
                # Limpiamos saltos de línea internos que Apple suele poner en sus títulos
                nombre = " ".join(nombre.split())
                
                if nombre and len(nombre) > 3:
                    contador += 1
                    print(f"{contador}. 📱 {nombre}")
                    
            if contador == 0:
                print("⚠️ No se encontraron elementos con los selectores estándar.")
                print("Nota: Apple cambia frecuentemente sus clases CSS o bloquea peticiones según el nodo de origen.")
            print("=" * 60)
            
        else:
            print(f"❌ Apple denegó el acceso o la página no existe. Código de estado: {response.status_code}")
            if response.status_code == 403:
                print("🛑 (Error 403: El sistema de protección perimetral de Apple ha bloqueado la petición del servidor de GitHub).")
                
    except Exception as e:
        print(f"❌ Ocurrió un error durante el scraping: {e}")

if __name__ == "__main__":
    extraer_dispositivos_apple()
