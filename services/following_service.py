from time import sleep
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
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
                self.checkActivity(excelFollowings)

            elif opcion == 3:
                print("Código a desarrollar")
                self.excel.checkMutual(excelFollowers, excelFollowings)

            elif opcion == 4:
                print("Código a desarrollar")
            
            elif opcion == 0:
                break


    def checkFixedPost(self):
        wait = WebDriverWait(self.driver, 10)
        #fixedPost = self.driver.find_elements(By.CSS_SELECTOR, 'svg[aria-label="Icono de publicación fijada"]')
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="Icono de publicación fijada"]')))
        except:
            pass
        fixedPost = self.driver.find_elements(By.CSS_SELECTOR, 'svg[aria-label="Icono de publicación fijada"]')

        return len(fixedPost)
    

    def checkStory(self):
        '''try:
            self.driver.find_element(By.CSS_SELECTOR, storyActive)
            return True
        except:
            return False
        '''
        return bool(self.driver.find_elements(By.CSS_SELECTOR, storyActive))
            
    

    def lastActivity(self, numCheckPost):
        publicaciones = self.driver.find_elements(By.CSS_SELECTOR, divPost)[:numCheckPost]

        if len(publicaciones) == 0:
            #story = self.checkStory()
            return None, "Si"

        fechas = []

        for publicacion in publicaciones:
            publicacion.click()
            sleep(5)
            fecha = self.driver.find_element(By.CSS_SELECTOR, "time.x1p4m5qa").get_attribute("datetime")
            
            fechaUTC = datetime.fromisoformat(fecha.replace("Z", "+00:00"))
            fechaSpain = fechaUTC.astimezone(ZoneInfo("Europe/Madrid"))
            #print(f"FECHA → {fecha}")
            fechas.append(fechaSpain)
            
            #self.driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="Cerrar"]').click()
            self.app.cerrarVentanaFollowX()
            #sleep(2)

        if max(fechas) < datetime.now(ZoneInfo("Europe/Madrid")) - timedelta(days=DIAS_INACTIVIDAD):
            inactiva = "Si"
        else:
            inactiva = "No"

        return max(fechas).strftime("%Y-%m-%d"), inactiva  
    

    def getBio(self):
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, infoBio)))
            
            try:
                botonMasBio = self.driver.find_element(By.CSS_SELECTOR, 'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.xyejjpt.x15dsfln.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x1yc453h')
                botonMasBio.click()
                sleep(1)
            except:
                pass

            bio = self.driver.find_elements(By.CSS_SELECTOR, infoBio)[0].text.replace("\n", " ")
        except:
            bio = ""

        return bio
        

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
            print(f"\n¡Bien! Has seguido a {numFollowings - lastNumberFollowings} cuenta/s nueva/s.")
        elif lastNumberFollowings > numFollowings:
            print(f"\nVaya, has dejado de seguir a {lastNumberFollowings - numFollowings} cuenta/s nueva/s.")
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

        if os.path.exists(excelFollowings) and os.path.exists(excelFollowingsOld):
            self.excel.checkFollowXChange(excelFollowings, excelFollowingsOld)
        
        print("\nProceso terminado. Volviendo al menú de Followings")


    def checkActivity(self, excelFollowings):
        print("\nVamos a comprobar la actividad de las cuentas que sigues, para detectar las cuentas inactivas.")
        print("\033[91m\n⚠️  ADVERTENCIA: Este proceso puede tardar bastante tiempo ya que debe analizar cada cuenta individualmente.\033[0m")

        confirmar = ""
        while confirmar not in ('S','N'):
            confirmar = input("\n¿Deseas continuar? (S/N): ").strip().upper()
            if confirmar == 'N':
                print("Proceso cancelado. Volviendo al menú anterior...")
                return
            elif confirmar not in ('S','N'):
                print("Opción incorrecta, introduce S o N")

        if not os.path.exists(excelFollowings):
            print("\nEl fichero de followings no existe, primero deberás ejecutar la opción número 1")
            return
        
        dfFollowings = pd.read_excel(excelFollowings)
        totalUsuarios = len(dfFollowings)

        for columna in ["Bio", "Ultima actividad", "Revisar"]:
            if columna not in dfFollowings.columns:
                dfFollowings[columna] = ""
            else:
                dfFollowings[columna] = dfFollowings[columna].fillna("").astype(str)

        dfFollowings.to_excel(excelFollowings, index=False)

        for idx, row in dfFollowings.iterrows():
            
            if idx != 0 and idx%10 == 0:
                print("\n-----------------------------")
                print(f"***Cuentas procesadas: {idx} de {totalUsuarios}***")
                print("-----------------------------\n")

            self.driver.get(row["Link"])

            print(f"\n==User: {row["Usuario"]}==")

            bio = self.getBio()

            story = self.checkStory()

            if story:
                #Si tiene story activa, asumimos que la fecha de actividad es el día que lanzamos el script.
                actividad = datetime.now(ZoneInfo("Europe/Madrid")).strftime("%Y-%m-%d")
                revisar = "No"
                print("La cuenta tiene historia/s activa/s")
            
            else:
                print("La cuenta no tiene historias activas, hay que comprobar las últimas publicaciones")
                
                numFijadas = self.checkFixedPost()

                if numFijadas == 0:
                    numCheckPost = 1
                else:
                    numCheckPost = numFijadas + 1

                actividad, revisar = self.lastActivity(numCheckPost)
            
            #Guardamos info en excel
            dfFollowings.at[idx, "Bio"] = bio
            dfFollowings.at[idx, "Ultima actividad"] = actividad if actividad else "Sin publicaciones"
            dfFollowings.at[idx, "Revisar"] = revisar
            dfFollowings.to_excel(excelFollowings, index=False)