import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def extraer_empleos():
    print("🚀 [CI/CD] Iniciando Extractor de Ofertas de Empleo...")
    url = "https://realpython.github.io/fake-jobs/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"📡 Conectando con {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Conexión exitosa. Analizando ofertas...")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos las "tarjetas" donde está la información de cada trabajo
            ofertas = soup.find_all("div", class_="card-content")
            
            fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
            
            # 📝 Abrimos un archivo CSV en modo escritura
            with open("ofertas_empleo.csv", mode="w", newline="", encoding="utf-8") as archivo_csv:
                # Configuramos el escritor CSV
                escritor = csv.writer(archivo_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                # Escribimos la cabecera (los nombres de las columnas)
                escritor.writerow(["Puesto", "Empresa", "Ubicación", "Fecha de Extracción"])
                
                print(f"\n💼 OFERTAS DE EMPLEO ENCONTRADAS")
                print("=" * 60)
                
                # Recorremos las primeras 15 ofertas para no hacer un archivo gigante en la prueba
                for i, oferta in enumerate(ofertas[:15], 1):
                    # Extraemos los datos usando las clases CSS de la web
                    titulo = oferta.find("h2", class_="title").text.strip()
                    empresa = oferta.find("h3", class_="company").text.strip()
                    ubicacion = oferta.find("p", class_="location").text.strip()
                    
                    # Lo mostramos por la consola de GitHub Actions
                    print(f"{i}. {titulo} en {empresa} ({ubicacion})")
                    
                    # Lo guardamos como una nueva fila en nuestro archivo CSV
                    escritor.writerow([titulo, empresa, ubicacion, fecha_actual])
                    
            print("=" * 60)
            print("💾 Archivo 'ofertas_empleo.csv' generado correctamente y listo para Git.")
            
        else:
            print(f"❌ Error al acceder a la web. Código de estado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")

if __name__ == "__main__":
    extraer_empleos()