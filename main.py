import sys
from core.app import InstagramApp
from config import *
from services.followers_service import FollowerService
from services.following_service import FollowingService

#Codificación de salida para la consola
sys.stdout.reconfigure(encoding='utf-8')

def main():

    app = InstagramApp()

    app.bienvenida(PROFILE_INSTAGRAM)

    while True:
        print("\n0 - Salir de la app")
        print("1 - Descargar vídeos/fotos de una colección")
        print("2 - Desmarcar guardados")
        print("3 - Herramientas para seguidores (followers)")
        print("4 - Herramientas para seguidos (followings)")
        print("5 - Comprobar último chequeo de followers")

        try:
            opcion = int(input("Elige opción: "))
            if opcion not in (0, 1, 2, 3, 4, 5):
                raise ValueError
        except ValueError:
            print("\nDebes introducir una opción correcta. Vuelve a probar.")
            continue
        if opcion == 1:
            print("Código a desarrollar")

        elif opcion == 2:
            print("Código a desarrollar")

        elif opcion == 3:
            #app.getFollowers(PROFILE_INSTAGRAM)
            FollowerService(app).getFollowers()

        elif opcion == 4:
            FollowingService(app).bannerFollowX()
            FollowingService(app).menuFollowings()

        elif opcion == 5:
            app.excel.checkUnfollow(excelFollowers, excelFollowersOld)
        
        elif opcion == 0:
            app.cerrar()
            break


if __name__ == "__main__":
    main()