import re


class Ejercicio2:
    def __init__(self):
        self.nombreclase = "Ejercicio2"

    def tostring(self):
        print(self.nombreclase)

    @staticmethod
    def validarpassword(password):
        try:
            print('')
            if len(password) < 8:
                print('Password menor de 8 caracteres.')
                return False
            if bool(re.search('^[a-zA-Z0-9]*$', password)) is True:
                print('El password no contiene caracteres especiales.')
                return False
            if bool(re.search('[a-z]', password)) is False:
                print('El password no contiene letras minúsculas')
                return False
            if bool(re.search('[A-Z]', password)) is False:
                print('El password no contiene letras mayusculas')
                return False
            if bool(re.search('[0-9]', password)) is False:
                print('El password no contiene números')
                return False
            print('La contraseña es válida')
            return True
        except (Exception,):
            print('Se ha generado una excepcion')
            return False
