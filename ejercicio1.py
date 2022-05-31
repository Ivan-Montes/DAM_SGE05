class Ejercicio1:
    def __init__(self):
        self.nombreclase = "Ejercicio1"

    def tostring(self):
        print(self.nombreclase)

    @staticmethod
    def validarnombre(cadena):
        try:
            print('')
            if len(cadena) < 6:
                print("El nombre de usuario debe contener al menos 6 caracteres.")
                return 1

            if len(cadena) > 12:
                print("El nombre de usuario no puede contener más de 12 caracteres")
                return 2

            if not cadena.isalnum():
                print("El nombre de usuario debe ser alfanumérico")
                return 3

            print('El nombre de usuario es válido')
            return 0
        except (Exception,):
            print('Se ha generado una excepcion')
            return 4

if __name__ == '__main__':
    foo = Ejercicio1()
    foo.validarnombre("hola")
