from config import *
from datetime import datetime
import os
import pandas as pd

class ExcelUtils:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path


    def creaExcel(self, fichero, columnas, ficheroOld):

        if os.path.exists(ficheroOld):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            newName = str(ficheroOld).replace(".xlsx", f"-{timestamp}.xlsx")
            os.rename(ficheroOld, newName)

        if os.path.exists(fichero):
            os.rename(fichero, ficheroOld)

        df = pd.DataFrame(columns=columnas)
        df.to_excel(fichero, index=False)