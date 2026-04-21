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
            print("\nEl fichero de control de followers/followings no existe, lo creo")
            if 'Followers' in str(fichero):
                df = pd.DataFrame(columns=["Número seguidores", "Fecha comprobación"])
            elif 'Followings' in str(fichero):
                df = pd.DataFrame(columns=["Número seguidos", "Fecha comprobación"])
            df.to_excel(fichero, index=False)
    

    def checkLastNumberFollowx(self, fichero, numFollowX):
        #Abrimos la excel de histórico y mantenemos en un dataframe
        dfCheckFollowX = pd.read_excel(fichero)
        dateActual = datetime.now().strftime("%d-%m-%Y %H:%M")

        #Comprobamos si está vacío para añadir directamente el valor actual, si no, leemos último registro
        if dfCheckFollowX.empty:
            #No hay registros
            with pd.ExcelWriter(fichero, mode='a', if_sheet_exists='overlay') as writer:
                if 'Followers' in str(fichero):
                    nuevoRegistro = pd.DataFrame([[numFollowX, dateActual]], columns=["Número seguidores", "Fecha comprobación"])
                    nuevoRegistro.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
                elif 'Followings' in str(fichero):
                    nuevoRegistro = pd.DataFrame([[numFollowX, dateActual]], columns=["Número seguidos", "Fecha comprobación"])
                    nuevoRegistro.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
            lastNumberFollowX = 0
            dateLastCheck = dateActual
        else:
            if 'Followers' in str(fichero):
                lastNumberFollowX = dfCheckFollowX.iloc[-1]["Número seguidores"]
            elif 'Followings' in str(fichero):
                lastNumberFollowX = dfCheckFollowX.iloc[-1]["Número seguidos"]
            #Comparamos seguidores/seguidos actuales con histórico
            if lastNumberFollowX == numFollowX:
                #Son iguales, solo actualizamos fecha
                dfCheckFollowX.iloc[-1, dfCheckFollowX.columns.get_loc("Fecha comprobación")] = dateActual
                dfCheckFollowX.to_excel(fichero, index=False)
            else:
                #Son distintos, añadimos nueva fila
                with pd.ExcelWriter(fichero, mode='a', if_sheet_exists='overlay') as writer:
                    if 'Followers' in str(fichero):
                        nuevoRegistro = pd.DataFrame([[numFollowX, dateActual]], columns=["Número seguidores", "Fecha comprobación"])
                        nuevoRegistro.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
                    elif 'Followings' in str(fichero):
                        nuevoRegistro = pd.DataFrame([[numFollowX, dateActual]], columns=["Número seguidos", "Fecha comprobación"])
                        nuevoRegistro.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
            dateLastCheck = dfCheckFollowX.iloc[-1]["Fecha comprobación"]

        return lastNumberFollowX, dateLastCheck


    def creaExcel(self, fichero, columnas, ficheroOld):
        if os.path.exists(ficheroOld):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            newName = str(ficheroOld).replace(".xlsx", f"-{timestamp}.xlsx")
            try:
                os.rename(ficheroOld, newName)
            except PermissionError:
                print(f"\nError: Cierra el fichero {fichero} antes de continuar.")
                input("Pulsa Enter cuando lo hayas cerrado...")
                os.rename(ficheroOld, newName)
            
            if not os.path.exists(folderOld):
                os.mkdir(folderOld)
            
            #Movemos los históricos a una carpeta concreta
            shutil.move(newName, folderOld)

        if os.path.exists(fichero):
            try:
                os.rename(fichero, ficheroOld)
            except PermissionError:
                print(f"\nError: Cierra el fichero {fichero} antes de continuar.")
                input("Pulsa Enter cuando lo hayas cerrado...")
                os.rename(fichero, ficheroOld)
        df = pd.DataFrame(columns=columnas)
        df.to_excel(fichero, index=False)

    
    def checkUnfollow(self, fichero, ficheroOld):
        dfNuevo = pd.read_excel(fichero)
        dfOld = pd.read_excel(ficheroOld)

        unfollows = dfOld[~dfOld["Link"].isin(dfNuevo["Link"])]

        print("\nAquí tienes el listado: ")

        for _, row in unfollows.iterrows():
            print(f"{row['Usuario']} · {row['Nombre']} · {row['Link']} · ¿Lo sigo? → {row['Lo sigo']}")