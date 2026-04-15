from core.app import InstagramApp
from config import PROFILE_INSTAGRAM




def main():

    app = InstagramApp()

    app.bienvenida(PROFILE_INSTAGRAM)

    while True:
        print("\n0 - Salir de la app")
        print("1 - Descargar vídeos/fotos de una colección")
        print("2 - Desmarcar guardados")
        print("3 - Herramientas para seguidores/siguiendo")

        try:
            opcion = int(input("Elige opción: "))
            if opcion not in (0, 1, 2, 3):
                raise ValueError
        except ValueError:
            print("\nDebes introducir una opción correcta. Vuelve a probar.")
            continue
        if opcion == 1:
            print("Código a desarrollar")

        elif opcion == 2:
            print("Código a desarrollar")

        elif opcion == 3:
            app.getFollowers(PROFILE_INSTAGRAM)
        
        elif opcion == 0:
            app.cerrar()
            break

if __name__ == "__main__":
    main()