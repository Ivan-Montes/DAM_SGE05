from ejercicio1 import Ejercicio1
from ejercicio2 import Ejercicio2


class Ejercicio3:
    def __init__(self):
        self.nombreclase = 'Ejercicio3'
        self.ejer1 = Ejercicio1()
        self.ejer2 = Ejercicio2()

    def tostring(self):
        print(self.nombreclase)

    def comenzar(self):
        try:
            print('#############')
            print(self.nombreclase)
            print('#############')
            print('')
            u = input('Introduzca el nombre de usuario: ')
            errorcode = self.ejer1.validarnombre(u)
            print('')
            print('Codigo devuelto: ', errorcode)
            print('')
            p = input('Introduzca contraseña: ')
            self.ejer2.validarpassword(p)
            print('')
        except (Exception,):
            print('Se ha generado una excepcion.')
            return False


if __name__ == '__main__':
    foo = Ejercicio3()
    foo.comenzar()
