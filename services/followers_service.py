from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class FollowerService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path
        self.excel = app.excel


    def getFollowers(self, url):
        ##Esta función obtiene el listado completo de las cuentas que te siguen
        print("Vamos a obtener tus seguidores")

        #Comprobamos si el fichero de histórico existe para crearlo si no. Creamos followers
        self.excel.controlFollowxExist(historicFollowers)
        followers = []

        #Comprobamos si estamos en la página del perfil para chequear followers, si no, vamos allí
        if self.driver.current_url != PROFILE_INSTAGRAM:
            print(f"Nos dirigimos a la URL de tu perfil: {PROFILE_INSTAGRAM}")
            self.driver.get(PROFILE_INSTAGRAM)

        #Recogemos el nº de followers actual
        spanFollowers = self.driver.find_element(By.XPATH, "//span[contains(text(), 'seguidores')]/span[@title]")
        numFollowers = int(spanFollowers.get_attribute("title").replace(",", "").replace(".", ""))

        lastNumberFollower, lastDateCheck = self.excel.checkLastNumberFollowx(historicFollowers,numFollowers)

        print (f"\nTienes actualmente un total de {numFollowers} seguidores.")

        if lastNumberFollower == 0:
            print("\nNo había registros previos")
        elif lastNumberFollower < numFollowers:
            print(f"\n¡Bien! Te ha/n seguido ({numFollowers - lastNumberFollower}) cuenta/s nueva/s.")
        elif lastNumberFollower > numFollowers:
            print(f"\nVaya, has perdido ({lastNumberFollower - numFollowers}) seguidor/es.")
        else:
            print(f"\nTienes los mismos seguidores que la última comprobación, hecha el {lastDateCheck}")


        self.driver.find_element(By.XPATH, "//*[contains(text(), 'seguidores')]").click()
        print("\nEspera mientras obtenemos tus seguidores. Esto puede tardar algunos minutos.")
        self.app.full_scroll_followX()

        listFollowers = self.driver.find_elements(By.CSS_SELECTOR, 'div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x2lah0s.x193iq5w.xeuugli.x1iyjqo2')
        
        for idx, follower in enumerate(listFollowers, start=1):            
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
        
        if followers:
            columnas = ["Usuario", "Nombre", "Link", "Lo sigo"]
            self.excel.creaExcel(excelFollowers, columnas, excelFollowersOld)
            df = pd.DataFrame(followers, columns=[columnas])
            with pd.ExcelWriter(excelFollowers, mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
        
        self.excel.checkUnfollow(excelFollowers, excelFollowersOld)