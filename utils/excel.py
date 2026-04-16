from config import *
from datetime import datetime
import os
import shutil
import pandas as pd

class ExcelUtils:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path


    def controlFollowxExist(self, fichero):
        if not os.path.exists(fichero):
            print("El fichero de control de followers no existe, lo creo")
            df = pd.DataFrame(columns=["Número seguidores", "Fecha comprobación"])
            df.to_excel(fichero, index=False)


    def checkLastNumberFollowx(self, fichero, numFollowers):
        #Abrimos la excel de histórico y mantenemos en un dataframe
        dfCheckFollowers = pd.read_excel(fichero)
        dateActual = datetime.now().strftime("%d-%m-%Y %H:%M")
        dateLastCheck = dfCheckFollowers.iloc[-1]["Fecha comprobación"]

        #Comprobamos si está vacío para añadir directamente el valor actual, si no, leemos último registro
        if dfCheckFollowers.empty:
            #No hay registros
            with pd.ExcelWriter(fichero, mode='a', if_sheet_exists='overlay') as writer:
                nuevoRegistro = pd.DataFrame([[numFollowers, dateActual]], columns=["Número seguidores", "Fecha comprobación"])
                nuevoRegistro.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
            lastNumberFollower = 0

        else:
            lastNumberFollower = dfCheckFollowers.iloc[-1]["Número seguidores"]
            #Comparamos seguidores actuales con histórico
            if lastNumberFollower == numFollowers:
                #Son iguales, solo actualizamos fecha
                dfCheckFollowers.iloc[-1, dfCheckFollowers.columns.get_loc("Fecha comprobación")] = dateActual
                dfCheckFollowers.to_excel(fichero, index=False)
            else:
                #Son distintos, añadimos nueva fila
                with pd.ExcelWriter(fichero, mode='a', if_sheet_exists='overlay') as writer:
                    nuevoRegistro = pd.DataFrame([[numFollowers, dateActual]], columns=["Número seguidores", "Fecha comprobación"])
                    nuevoRegistro.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
            
        return lastNumberFollower, dateLastCheck



    def creaExcel(self, fichero, columnas, ficheroOld):
        '''
        if os.path.exists(ficheroOld):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            newName = str(ficheroOld).replace(".xlsx", f"-{timestamp}.xlsx")
            os.rename(ficheroOld, newName)
            
            if not os.path.exists(folderOld):
                os.mkdir(folderOld)
            
            #Movemos los históricos a una carpeta concreta
            shutil.move(newName, folderOld)

        if os.path.exists(fichero):
            os.rename(fichero, ficheroOld)
        '''
        df = pd.DataFrame(columns=columnas)
        df.to_excel(fichero, index=False)

    
    def checkUnfollow(self, fichero, ficheroOld):
        dfNuevo = pd.read_excel(fichero)
        dfOld = pd.read_excel(ficheroOld)

        unfollows = dfOld[~dfOld["Link"].isin(dfNuevo["Link"])]

        for link in unfollows["Link"]:
            print(link)