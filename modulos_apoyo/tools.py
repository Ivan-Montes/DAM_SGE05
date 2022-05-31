import random
import time


class Tools:

    def __init__(self):
        self.name = "Tools"

    @staticmethod
    def titulo(msg: str):
        print('##################')
        print(msg)
        print('##################')
        print('')

    @staticmethod
    def pedirdato(mensaje):
        leido = input(mensaje)
        return leido

    @staticmethod
    def pulseintro():
        input("Presione INTRO para continuar...")

    @staticmethod
    def crearloginusuario(nombre: str):
        nombresplit = nombre.lower().split(' ')
        login = nombresplit[0][0:1] + nombresplit[1]
        return login

    @staticmethod
    def crearpassword(nombre: str):
        passwd = 'Cam5iar$'
        try:
            nombresplit = nombre.split(' ')
            random.shuffle(nombresplit)
            primerelemento: str = nombresplit[0][0:1]
            segundos: str = str(time.localtime().tm_sec)
            tercerelemento: str = nombresplit[1][1:2]
            cuartoelemento: str = nombresplit[1][2:3].upper()
            minutos: str = str(time.localtime().tm_min)
            quintoelemento: str = nombresplit[2][3:4]
            simbolos = ['%', '&', '$']
            random.shuffle(simbolos)
            sextoelemento: str = simbolos[0]
            print('## Creación de la contraseña')
            print(nombresplit)
            print(primerelemento)
            print(segundos)
            print(tercerelemento)
            print(cuartoelemento)
            print(minutos)
            print(quintoelemento)
            print(sextoelemento)

            passwd = primerelemento + segundos + tercerelemento + cuartoelemento + minutos \
                + quintoelemento + sextoelemento
        except(Exception,):
            print('Excepcion al crear la contraseña. Se establece contraseña por defecto => Cam5iar$')
            passwd = 'Cam5iar$'
        finally:
            if len(passwd) < 8:
                passwd = 'Cam5iar$'
        return passwd
