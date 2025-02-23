# pip install selenium textblob
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from textblob import TextBlob

# Función para clasificar el sentimiento
def clasificar_sentimiento(texto):
    analisis = TextBlob(texto)
    polaridad = analisis.sentiment.polarity

    if polaridad > 0:
        return "positivo"
    elif polaridad < 0:
        return "negativo"
    else:
        return "neutro"

# Función para eliminar publicidades y elementos no deseados
def eliminar_publicidades(driver):
    try:
        # Lista de selectores CSS para eliminar publicidades y elementos no deseados
        elementos_a_eliminar = [
            "Contacto",
            "COMUNICA",
            "PUBLICIDAD",
            "iframe",  # Eliminar iframes (a menudo contienen anuncios)
            "div[class*='ad']",  # Eliminar divs con clases que contengan "ad"
            "div[id*='ad']",  # Eliminar divs con IDs que contengan "ad"
            "script",  # Eliminar scripts
            "style",  # Eliminar estilos
            "footer",  # Eliminar el pie de página
            "nav",  # Eliminar barras de navegación
            "aside",  # Eliminar barras laterales (a menudo contienen anuncios)
            "header",  # Eliminar la cabecera
            "form",  # Eliminar formularios
            "button",  # Eliminar botones
            "img",  # Eliminar imágenes
            "a",  # Eliminar enlaces
        ]

        for selector in elementos_a_eliminar:
            elementos = driver.find_elements(By.CSS_SELECTOR, selector)
            for elemento in elementos:
                driver.execute_script("""
                    var elemento = arguments[0];
                    elemento.parentNode.removeChild(elemento);
                """, elemento)
    except Exception as e:
        print(f"Error al eliminar publicidades: {e}")

# Configura el driver de Selenium (asegúrate de que ChromeDriver esté en tu PATH)
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    # URL inicial (Google)
    driver.get("https://www.google.com")
    time.sleep(random.uniform(2, 4))  # Retraso aleatorio para simular comportamiento humano

    # Buscar información sobre el deslave de La Mana, Ecuador, 30 de enero de 2022
    search_query = "deslave La Mana Ecuador 30 de enero de 2022"
    search_box = driver.find_element(By.NAME, "q")
    for char in search_query:
        search_box.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))  # Escribir la consulta de manera más humana
    search_box.send_keys(Keys.RETURN)
    time.sleep(random.uniform(3, 5))

    # Recopilar enlaces de las primeras fuentes
    sources = []
    while len(sources) < 20:
        # Obtener resultados actuales
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        for result in results:
            try:
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                if link not in sources:
                    sources.append(link)
                    if len(sources) >= 20:
                        break
            except Exception as e:
                print(f"Error al obtener un enlace: {e}")

        # Intentar pasar a la siguiente página si no se han recopilado 20 fuentes aún
        try:
            next_button = driver.find_element(By.ID, "pnnext")
            next_button.click()
            time.sleep(random.uniform(3, 5))  # Retraso aleatorio
        except Exception:
            print("No se encontró el botón para la siguiente página o se alcanzó el final de los resultados.")
            break

    print(f"Se recopilaron {len(sources)} fuentes.")
    print("-" * 80)

    # Visitar cada enlace y extraer información
    data = []  # Lista para almacenar los datos en formato JSON
    for i, source in enumerate(sources, start=1):
        print(f"Extrayendo información de la fuente {i}: {source}")
        try:
            driver.get(source)
            time.sleep(random.uniform(3, 5))  # Retraso aleatorio

            # Eliminar publicidades y elementos no deseados
            eliminar_publicidades(driver)

            # Extraer el contenido principal de la página (parágrafos)
            paragraphs = driver.find_elements(By.TAG_NAME, "p")
            page_content = " ".join([p.text for p in paragraphs if p.text.strip()])

            # Si no hay contenido, omitir este registro
            if not page_content.strip():
                print(f"Fuente {i} no tiene contenido. Omitiendo...")
                continue

            # Realizar análisis de sentimientos
            sentimiento = clasificar_sentimiento(page_content)

            # Guardar información en formato JSON
            data.append({
                "id": i,
                "url": source,
                "content": page_content[:500],  # Limitamos el contenido a los primeros 500 caracteres
                "sentimiento": sentimiento
            })
            print(f"Fuente {i} procesada correctamente. Sentimiento: {sentimiento}")
        except Exception as e:
            print(f"Error al extraer contenido de la fuente {i}: {e}")
        finally:
            print("-" * 80)

    # Guardar los datos en un archivo JSON
    with open("deslave_la_mana_30_enero_2022_limpio.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("La información se guardó en el archivo 'deslave_la_mana_30_enero_2022_limpio.json'.")

except Exception as e:
    print(f"Error general: {e}")
finally:
    driver.quit()