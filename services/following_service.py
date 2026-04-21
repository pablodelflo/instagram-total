from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import re

class FollowingService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path
        self.excel = app.excel


    def bannerFollowX(self):
        ##Esta función mostrará en pantalla el banner de bienvenida con el nombre del usuario y abrirá su perfil en IG

        #Comprobamos si estamos en la página del perfil para chequear followings, si no, vamos allí
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
                self.getFollowings()

            elif opcion == 2:
                print("Código a desarrollar")

            elif opcion == 3:
                print("Código a desarrollar")
                self.excel.checkMutual(excelFollowers, excelFollowings)

            elif opcion == 4:
                print("Código a desarrollar")
            
            elif opcion == 0:
                break

    def getFollowings(self):
        ##Esta función obtiene el listado completo de las cuentas que sigues
        print("\nVamos a obtener tus seguidos")

        #Comprobamos si el fichero de histórico existe para crearlo si no. Creamos Followings
        self.excel.controlFollowxExist(historicFollowings)
        followings = []
        
        #Comprobamos si estamos en la página del perfil para chequear Followings, si no, vamos allí
        if self.driver.current_url != PROFILE_INSTAGRAM:
            print(f"\nNos dirigimos a la URL de tu perfil: {PROFILE_INSTAGRAM}")
            self.driver.get(PROFILE_INSTAGRAM)

        #Recogemos el nº de followings actual
        spanFollowings = self.driver.find_element(By.XPATH, "//span[contains(text(), 'seguidos')]")
        numFollowings = int(re.search(r"\d+", spanFollowings.text).group())

        lastNumberFollowings, lastDateCheck = self.excel.checkLastNumberFollowx(historicFollowings,numFollowings)

        print (f"\nSigues actualmente a {numFollowings} cuenta/s.")

        if lastNumberFollowings == 0:
            print("\nNo había registros previos")
        elif lastNumberFollowings < numFollowings:
            print(f"\n¡Bien! Has seguido a ({numFollowings - lastNumberFollowings}) cuenta/s nueva/s.")
        elif lastNumberFollowings > numFollowings:
            print(f"\nVaya, has dejado de seguir a ({lastNumberFollowings - numFollowings}) cuenta/s nueva/s.")
        else:
            print(f"\nSigues al mismo número de cuentas que la última vez, hecha el {lastDateCheck}")

        self.driver.find_element(By.XPATH, "//*[contains(text(), 'seguidos')]").click()
        print("\nEspera mientras obtenemos tus seguidos. Esto puede tardar algunos minutos.")
        self.app.full_scroll_followX()

        listFollowings = self.driver.find_elements(By.CSS_SELECTOR, 'div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x2lah0s.x193iq5w.xeuugli.x1iyjqo2')
        
        for idx, following in enumerate(listFollowings, start=1):            
            userName = following.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href").strip("/").split("/")[-1]
            nombreReal = following.find_element(By.CSS_SELECTOR, "span.x1lliihq.x193iq5w").text
            link = following.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href")
            
            followings.append([userName, nombreReal, link, ""])
        
        if followings:
            columnas = ["Usuario", "Nombre", "Link", "Mutual"]
            self.excel.creaExcel(excelFollowings, columnas, excelFollowingsOld)
            df = pd.DataFrame(followings, columns=[columnas])
            with pd.ExcelWriter(excelFollowings, mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
        
        print("\nProceso terminado. Volviendo al menú de Followings")