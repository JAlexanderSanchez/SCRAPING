Proyecto: Web Scraping con Selenium

Descripción

Este proyecto utiliza Selenium para realizar web scraping de resultados de búsqueda en Google. Se centra en recopilar información sobre un evento específico (deslave en La Mana, Ecuador, el 30 de enero de 2022) y extraer el contenido de las páginas obtenidas en los resultados de búsqueda. Los datos recopilados se almacenan en un archivo JSON para su posterior análisis.

Requisitos de Instalación

Antes de ejecutar el script, asegúrate de tener instaladas las siguientes dependencias en tu entorno de Python:

1. Instalar Selenium

pip install selenium

Selenium es una biblioteca que permite automatizar navegadores web para la extracción de datos y pruebas automatizadas.

2. Instalar TextBlob (Opcional)

pip install textblob

TextBlob se puede utilizar para el procesamiento de texto, análisis de sentimientos y manipulación del contenido extraído.

3. Descarga e instalación de ChromeDriver

Para ejecutar Selenium con Chrome, necesitas descargar e instalar ChromeDriver:

Descarga ChromeDriver desde: https://sites.google.com/chromium.org/driver/

Asegúrate de que la versión de ChromeDriver coincida con la versión de Google Chrome instalada en tu sistema.

Añade ChromeDriver a tu variable de entorno PATH o colócalo en el mismo directorio que el script de Python.

Funcionamiento del Script

El script realiza las siguientes tareas:

Abre un navegador con Selenium y accede a Google.

Realiza una búsqueda con la consulta: "deslave La Mana Ecuador 30 de enero de 2022".

Extrae hasta 20 enlaces de los resultados de búsqueda.

Visita cada enlace y extrae el contenido de los párrafos.

Guarda los datos extraídos en un archivo JSON llamado deslave_la_mana_30_enero_2022.json.

Cierra el navegador al finalizar.

Ejecución del Script

Para ejecutar el script, simplemente corre el siguiente comando en tu terminal o línea de comandos:

python script.py

(Sustituye script.py con el nombre real de tu archivo Python).

Notas Adicionales

Se han añadido pausas aleatorias en la escritura de la consulta y la navegación entre páginas para simular un comportamiento humano y evitar bloqueos por parte de Google.

Se recomienda usar proxies o configurar un User-Agent personalizado para reducir el riesgo de detección.
