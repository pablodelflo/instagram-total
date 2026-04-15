from pathlib import Path
from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


    def full_scroll(self, pausa=1):
        ##Esta función fuerza el scroll vertical para asegurar la carga de todos los elementos (vídeos, colecciones, etc)
        # Obtener altura inicial
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Hacer scroll al final
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)

            # Comparar altura después del scroll
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                print("📉 Fin del scroll detectado, forzando scrolls adicionales...")
                
                # Hacer scrolls adicionales forzados
                for i in range(MAX_EXTRA_SCROLLS):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(SCROLL_PAUSE_TIME)
                
                # Una última comprobación
                final_height = self.driver.execute_script("return document.body.scrollHeight")
                if final_height == last_height:
                    print("✅ Scroll final confirmado.")
                    break
                else:
                    print("🔁 Scroll reactivado, continuando...")
                    last_height = final_height
            else:
                last_height = new_height


    def full_scroll_followX(self, pausa=1):
        wait = WebDriverWait(self.driver, 15)
        scroll_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, followers_list)))

        prev_height = 0
        while True:
            current_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll_div)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_div)
            sleep(5)  # espera a que cargue nuevo contenido
            new_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll_div)
            if new_height == current_height:
                break


    def getFollowers(self, url):
        ##Esta función obtiene el listado completo de las cuentas que te siguen
        print("Vamos a obtener tus seguidores")

        if self.driver.current_url != PROFILE_INSTAGRAM:
            print(f"Nos dirigimos a la URL de tu perfil: {PROFILE_INSTAGRAM}")
            self.driver.get(PROFILE_INSTAGRAM)

        self.driver.find_element(By.XPATH, "//*[contains(text(), 'seguidores')]").click()
        self.full_scroll_followX()