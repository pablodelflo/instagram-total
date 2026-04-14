#Renombra este archivo a config.py y luego edítalo con tus configuraciones personalizadas.

from pathlib import Path
BASE_PATH_COLECCIONES = Path("C:/ruta/donde-guardar/colecciones")
DEBUG_PORT = "127.0.0.1:9222"
PROFILE_TIKTOK = "https://www.instagram.com/username/"  # Reemplaza con el perfil de Instagram que deseas analizar
SCROLL_PAUSE_TIME = 2.5 # Pausa entre scrolls (en segundos) para que no se detecte como un bot
MAX_EXTRA_SCROLLS = 2  # Scrolls adicionales después del final
MAX_THREADS = 4 # Número máximo de hilos para procesar en paralelo

##CLASES CSS PARA SCRAPPING##
#---------------------------#
#Aquí puedes agregar las clases CSS que se utilizan para el scrapping. Por ejemplo: