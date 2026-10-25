from time import sleep
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from config import *
from urllib.parse import urlparse
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

class VideoService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path

    
    def descargaVideos(self, videos, pathColeccion, MAX_THREADS):
        print(videos)

        rutaVideos = pathColeccion / "videos"
        print("\n==Iniciamos la descarga de vídeos==")

        if not os.path.exists(rutaVideos):
            os.mkdir(rutaVideos)

        for video in videos:
            links = video["url"]
            
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            tareas = [
                executor.submit(self.descargarUnVideo, link, rutaVideos)
                for link in links
            ]

            for f in tqdm(as_completed(tareas), total=len(links), desc="Descargando vídeos", unit=" video/s"):
                resultado = f.result()
                if resultado:
                    tqdm.write(resultado)

    
    def descargarUnVideo(self, link, rutaVideos):
        #print(f"Descargando {link}")
        #return f"Descargado: {link}"
    
        errorMsg = "impersonation"

        #try:


'''
def descargar_un_video(self, video, full_path_video):
        txt_error = "impersonation"

        try:
            full_name = self.app.info_video(video)
            full_name_video = f"{full_name}.mp4"

            comando = [
                "py", "-3.11", "-m", "yt_dlp",
                "--cookies", "cookies.txt",
                "-o", full_name_video,
                "-P", str(full_path_video),
                video,
                "-q"
            ]

            comandoV2 = [
                "py", "-3.11", "-m", "yt_dlp",
                "--cookies-from-browser", "firefox",
                "-o", full_name_video,
                "-P", str(full_path_video),
                video,
                "-q"
            ]

            result = subprocess.run(comando, capture_output=True, text=True)
            if result.returncode != 0 and txt_error in result.stderr.strip():
                print(f"\n❌ Error con {full_name_video}: {result.stderr.strip()}")
                print("\n==Vamos a probar el método alternativo de descarga==")
                resultV2 = subprocess.run(comandoV2, capture_output=True, text=True)
                if resultV2.returncode != 0:
                    return f"❌ Error con {full_name_video}: {result.stderr.strip()}"
            
            return f"✅ Descargado: {full_name_video}"
        
        except Exception as e:
            return f" Error procesando: {video} → {e}" 
'''