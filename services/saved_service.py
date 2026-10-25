from time import sleep
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from config import *
from services.videos_service import VideoService
from urllib.parse import urlparse
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import re

class SavedService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path
        self.video_service = VideoService(app)


    def bannerSaved(self):
        ##Esta función mostrará en pantalla el banner de bienvenida con el nombre del usuario y abrirá su perfil en IG

        #Comprobamos si estamos en la página del perfil para chequear followings, si no, vamos allí
        if self.driver.current_url != SAVED_INSTAGRAM:
            print(f"Nos dirigimos a la URL de tus elementos guardados: {SAVED_INSTAGRAM}")
            self.driver.get(SAVED_INSTAGRAM)

        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n========== INSTAGRAM TOTAL ==============")
        print("\n* Herramientas para elementos guardados *\n")
        print("=========================================")

    
    def menuSaved(self):
        while True:
            print("\n0 - Volver al menú principal")
            print("1 - Listar colecciones")
            print("2 - Descargar colección")
            print("3 - Desmarcar guardados")

            try:
                opcion = int(input("Elige opción: "))
                if opcion not in (0, 1, 2, 3):
                    raise ValueError
            except ValueError:
                print("\nDebes introducir una opción correcta. Vuelve a probar.")
                continue
            if opcion == 1:
                self.getCollections()

            elif opcion == 2:
                print("A desarrollar")

            elif opcion == 3:
                print("A desarrollar")
            
            elif opcion == 0:
                break

    
    def getCollections(self):
        #Guardo colecciones como atributo de clase para poder usarla en otras
        self.colecciones = []

        haveCollections = self.driver.find_elements(By.CSS_SELECTOR, TIENECOLECCIONES)
        if not haveCollections:
            print("\n==No tienes colecciones creadas==")
            return None
        
        print("\nEspera mientras obtengo el listado completo.")
        self.app.full_scroll()

        collections = self.driver.find_elements(By.CSS_SELECTOR, COLECCIONES) 

        print("\nEstas son tus colecciones:")

        for idx, collection in enumerate(collections, start=1):
            nombreCollection = collection.find_element(By.CSS_SELECTOR, NOMBRECOLECCION).text
            linkCollection = collection.find_element(By.CSS_SELECTOR, "a")
            url = linkCollection.get_attribute("href")
            self.colecciones.append({
                "id": idx,
                "nombre": nombreCollection,
                "url": url
            })

        if self.colecciones:
            self.imprimeColecciones(self.colecciones)

        descargar = ""
        while descargar not in ('S','N'):
            descargar = input("\n¿Quieres descargar alguna de las colecciones? (S/N): ").strip().upper()
            if descargar == 'N':
                print("Proceso cancelado. Volviendo al menú anterior...")
                return None
            elif descargar not in ('S','N'):
                print("Opción incorrecta, introduce S o N")

        print("\nOk, vamos a ello.")
        self.descargaColeccion()        

        return self.colecciones


    def imprimeColecciones(self, colecciones):
        for idx, coleccion in enumerate(colecciones, start=1):
            print(f"{coleccion['id']} - {coleccion['nombre'].title()} → URL: {coleccion['url']}")


    def obtenerUrl(self, elementosGuardados, descriptions, hayVideos, hayFotos, pathColeccion):
        if hayVideos:
            videosTxt = pathColeccion / "videos.txt"

        if hayFotos:
            fotosTxt = pathColeccion / "fotos.txt"

        if descriptions:
            descripcionPath = pathColeccion / "Descripciones"

        publicaciones = []

        for publicacion in elementosGuardados:
            url = publicacion.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            autor = ""
            
            publicacion.click()
            wait = WebDriverWait(self.driver, 10)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, NOMBREAUTOR)))
                autor = self.driver.find_elements(By.CSS_SELECTOR, NOMBREAUTOR)[0].text
            except:
                pass
            self.app.cerrarVentanaFollowX()

            if publicacion.find_elements(By.CSS_SELECTOR, CLIPGUARDADO) or publicacion.find_elements(By.CSS_SELECTOR, VIDEOGUARDADO):
                tipoElemento = 'video'
            elif publicacion.find_elements(By.CSS_SELECTOR, SLIDERGUARDADO):
                tipoElemento = 'foto'
            else:
                tipoElemento = 'foto'

            path = urlparse(url).path
            partes = path.split("/")
            videoID = partes[2]

            publicaciones.append({
                "url": url,
                "autor": autor,
                "tipoElemento": tipoElemento,
                "videoID": videoID
            })

            if descriptions:
                descripcion = publicacion.find_element(By.XPATH, ".//img").get_attribute("alt")
                self.saveDescripcion(descripcion, descripcionPath, autor, videoID)      
        
        print("He finalizado la obtención de enlaces de la colección")
        print("\nProcedemos a descargar los elementos")

        videos = [v for v in publicaciones if v["tipoElemento"] == "video"]
        fotos = [f for f in publicaciones if f["tipoElemento"] == "fotos"]

        if len(videos) > 0:
            self.video_service.descargaVideos(videos, pathColeccion, MAX_THREADS)
            



        



    

    def saveDescripcion(self, descripcion, descripcionPath, autor, videoID):
        if not os.path.exists(descripcionPath):
            os.mkdir(descripcionPath)
        
        nombreDescripcion = f"{autor} - {videoID}.txt"
        pathDescripcion = descripcionPath / f"{nombreDescripcion}"
        with pathDescripcion.open("w", encoding="utf-8") as desc:
            desc.write(descripcion)

    
    def descargaColeccion(self):
        if not self.colecciones:
            print("\nPrimero debes comprobar tus colecciones guardadas.")
            return None
        
        print("\n==Si deseas volver al menú principal, pulsa 0==")

        while True:
            try:
                coleccionDescarga = int(input("\nIntroduce el ID de la colección a descargar: "))
            except ValueError:
                print("Debes introducir un número válido.")
                continue
            
            if coleccionDescarga == 0:
                print("\nVolviendo al menú principal")
                return None
            elif coleccionDescarga == 1:
                print("\nLo siento, \"Todas las publicaciones\" no es una colección válida.")
            elif coleccionDescarga < 0 or coleccionDescarga > len(self.colecciones):
                print(f"\nDebes introducir un número entre 1 y {len(self.colecciones)}")
            else:
                idColeccion = coleccionDescarga - 1
                print(f"\nOk, accedemos a la colección {self.colecciones[idColeccion]['nombre']}")
                break

        self.driver.get(self.colecciones[idColeccion]['url'])
        coleccionName = self.colecciones[idColeccion]['nombre']

        pathColeccion = BASE_PATH_COLECCIONES / coleccionName

        if not os.path.exists(pathColeccion):
                os.mkdir(pathColeccion)

        print("\nObteniendo el número total de vídeos de esta colección...")
        self.app.full_scroll()
        elementosGuardados = self.driver.find_elements(By.CSS_SELECTOR, ELEMENTOGUARDADO)
        slidersGuardados = self.driver.find_elements(By.CSS_SELECTOR, SLIDERGUARDADO)
        videosGuardados = self.driver.find_elements(By.CSS_SELECTOR, VIDEOGUARDADO)
        videosGuardados += self.driver.find_elements(By.CSS_SELECTOR, CLIPGUARDADO)
        fotosGuardadas = (len(elementosGuardados) - (len(slidersGuardados)+len(videosGuardados)))
        print(f"\nLa colección {coleccionName} tiene {len(elementosGuardados)} elementos guardados:")
        print(f"{len(slidersGuardados)} sliders, {len(videosGuardados)} vídeos y {fotosGuardadas} fotos.")

        hayVideos = hayFotos = False
        
        if len(videosGuardados) > 0:
            hayVideos = True
        
        if fotosGuardadas > 0 or len(slidersGuardados) > 0:
            hayFotos = True

        descripciones = ""
        descriptions = False

        while descripciones not in ('S','N'):
            descripciones = input("\n¿Quieres descargar las descripciones de los elementos guardados? (S/N): ").strip().upper()
            if descripciones == 'N':
                print("Ok, descargamos los elementos guardados sin descripciones...")
            elif descripciones == 'S':
                print("De acuerdo, descargamos las descripciones.")
                descriptions = True
            elif descripciones not in ('S','N'):
                print("Opción incorrecta, introduce S o N")

        print("\nEspera mientras obtenemos las urls de los elementos guardados")
        self.obtenerUrl(elementosGuardados, descriptions, hayVideos, hayFotos, pathColeccion)

