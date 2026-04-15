from pathlib import Path
from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from time import sleep
import re
import os
from pathlib import Path

class InstagramApp:

    def __init__(self):
        self.base_path = Path (BASE_PATH_COLECCIONES)
        self.driver = get_driver()


    def cerrar(self):
        print("\nSaliendo de la app... ¡Hasta la próxima!")
        self.driver.quit()

    
    def bienvenida(self, url):
        ##Esta función mostrará en pantalla el banner de bienvenida con el nombre del usuario y abrirá su perfil en IG
        self.driver.get(url)

        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n================ INSTAGRAM TOTAL =================")
        print("\n* Una app en Python para gestionar tu red social *\n")
        print("==================================================")