#Renombra este archivo a config.py y luego edítalo con tus configuraciones personalizadas.

from pathlib import Path
BASE_PATH_COLECCIONES = Path("C:/ruta/donde-guardar/colecciones")
DEBUG_PORT = "127.0.0.1:9222"
PROFILE_INSTAGRAM = "https://www.instagram.com/username/"  # Reemplaza con tu perfil de Instagram que deseas analizar
SCROLL_PAUSE_TIME = 2.5 # Pausa entre scrolls (en segundos) para que no se detecte como un bot
MAX_EXTRA_SCROLLS = 2  # Scrolls adicionales después del final
MAX_THREADS = 4 # Número máximo de hilos para procesar en paralelo
DIAS_INACTIVIDAD = 60 # Número de días para considerar una cuenta como inactiva

##FICHEROS
#Completa la ruta de los siguientes ficheros excel. Deben estar dentro de la carpeta UTILS
excelFollowers = Path("")
excelFollowings = Path("")
excelFollowersOld = Path("")
excelFollowingsOld = Path("")
lastFollowers = Path("")
lastFollowings = Path("")
folderOld = Path("")

##CLASES CSS PARA SCRAPPING##
#---------------------------#
#Aquí puedes agregar las clases CSS que se utilizan para el scrapping. Por ejemplo:
#Popup followers
followers_list = 'div.x6nl9eh.x1a5l9x9.x7vuprf.x1mg3h75.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6'

#Bio usuario
infoBio = 'span._ap3a._aaco._aacu._aacx._aad7._aade'

#DIV publicaciones
divPost = 'div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x14z9mp.xhe4ym4.xaudc5v.x1j53mea'

#Story
storyActive = 'canvas.x1upo8f9.xpdipgo.x87ps6o'