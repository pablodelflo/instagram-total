from pathlib import Path
from config import *
from utils.excel import ExcelUtils
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from time import sleep
import re
import os
from pathlib import Path
import pandas as pd

class InstagramApp:

    def __init__(self):
        self.base_path = Path (BASE_PATH_COLECCIONES)
        self.driver = get_driver()
        self.excel = ExcelUtils(self)


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
        vuelta = 0
        while True:
            current_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll_div)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_div)
            sleep(5)  # espera a que cargue nuevo contenido
            new_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll_div)
            if new_height == current_height:
                break
            vuelta = vuelta + 1
            if vuelta == 2:
                break  # DEBUG: solo un scroll


    def getFollowers(self, url):
        ##Esta función obtiene el listado completo de las cuentas que te siguen
        print("Vamos a obtener tus seguidores")

        if self.driver.current_url != PROFILE_INSTAGRAM:
            print(f"Nos dirigimos a la URL de tu perfil: {PROFILE_INSTAGRAM}")
            self.driver.get(PROFILE_INSTAGRAM)

        followers = []
        spanFollowers = self.driver.find_element(By.XPATH, "//span[contains(text(), 'seguidores')]/span[@title]")
        numFollowers = int(spanFollowers.get_attribute("title").replace(",", "").replace(".", ""))

        print (f"Tienes actualmente un total de {numFollowers} seguidores. ")

        self.driver.find_element(By.XPATH, "//*[contains(text(), 'seguidores')]").click()
        self.full_scroll_followX()

        listFollowers = self.driver.find_elements(By.CSS_SELECTOR, 'div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x2lah0s.x193iq5w.xeuugli.x1iyjqo2')
        
        for idx, follower in enumerate(listFollowers, start=1):
            # Asumiendo que 'elemento' es cada bloque de usuario en la lista
            userName = follower.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href").strip("/").split("/")[-1]
            nombreReal = follower.find_element(By.CSS_SELECTOR, "span.x1lliihq.x193iq5w").text
            link = follower.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href")
            try:
                loSigo = follower.find_element(By.CSS_SELECTOR, 'div._ap3a._aacn._aacw._aad6').text
            except:
                loSigo = ""

            if loSigo:
                estadoReciproco = "No"    
            else:
                estadoReciproco = "Si"

            followers.append([userName, nombreReal, link, estadoReciproco])

            print(f"\n{userName} {nombreReal} {link} {estadoReciproco}")
        
        if followers:
            columnas = ["Usuario", "Nombre", "Link", "Lo sigo"]
            self.excel.creaExcel(excelFollowers, columnas, excelFollowersOld)
            df = pd.DataFrame(followers, columns=[columnas])
            with pd.ExcelWriter(excelFollowers, mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)