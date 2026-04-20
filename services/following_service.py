from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

class FollowingService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path
        self.excel = app.excel


    def bannerFollowX(self, url):
        ##Esta función mostrará en pantalla el banner de bienvenida con el nombre del usuario y abrirá su perfil en IG

        #Comprobamos si estamos en la página del perfil para chequear followers, si no, vamos allí
        if self.driver.current_url != PROFILE_INSTAGRAM:
            print(f"Nos dirigimos a la URL de tu perfil: {PROFILE_INSTAGRAM}")
            self.driver.get(PROFILE_INSTAGRAM)

        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n========== INSTAGRAM TOTAL ===========")
        print("\n* Análisis de seguidos (followings) *\n")
        print("======================================")

    
    def menuFollowings(self):
        while True:
            print("\n0 - Volver al menú principal")
            print("1 - Obtener lista de cuentas a la que sigues")
            print("2 - Comprobar cuentas inactivas")
            print("3 - Comprobar mutuals (followbacks)")
            print("4 - Análisis completo")

            try:
                opcion = int(input("Elige opción: "))
                if opcion not in (0, 1, 2, 3, 4):
                    raise ValueError
            except ValueError:
                print("\nDebes introducir una opción correcta. Vuelve a probar.")
                continue
            if opcion == 1:
                print("Código a desarrollar")

            elif opcion == 2:
                print("Código a desarrollar")

            elif opcion == 3:
                print("Código a desarrollar")

            elif opcion == 4:
                print("Código a desarrollar")
            
            elif opcion == 0:
                break
  

    def getFollowings(self, url):
        print("\n¡ATENCIÓN! Estás a punto de lanzar un proceso completo")