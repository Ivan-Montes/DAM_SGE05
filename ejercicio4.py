import csv


class Ejercicio4:
    def __init__(self):
        self.nombreclase = 'Ejercicio4'
        self.tabla = {}

    def comenzar(self):
        try:
            self.presentacion()

            while True:
                self.menuinicial()
                opcionmenu = self.pedirdato('Introduzca el numero de opción: ')

                if opcionmenu == "0":
                    print('Opción 0, salimos')
                    break
                elif opcionmenu == "1":
                    self.introducirdatos()
                elif opcionmenu == "2":
                    self.buscardatos()
                elif opcionmenu == "3":
                    self.agregardatosacsv()
                elif opcionmenu == "4":
                    self.recuperardatos()
                else:
                    print('Opción erronea, vuelva a probar')
        except (Exception,):
            print('Se ha generado una excepcion')
        finally:
            print('')

    def presentacion(self):
        print('#############')
        print(self.nombreclase)
        print('#############')

    @staticmethod
    def menuinicial():
        print('')
        print('1) Introducir datos')
        print('2) Buscar por nombre o apellido')
        print('3) Añadir a un CSV')
        print('4) Recuperar de un CSV')
        print('0) Salir')
        print('')

    @staticmethod
    def pedirdato(mensaje):
        leido = input(mensaje)
        return leido

    @staticmethod
    def pulseintro():
        input("Presione INTRO para continuar...")

    def introducirdatos(self):
        print('')
        print('### Introducir datos ###')
        apellidos = Ejercicio4.pedirdato('Introduzca los apellidos: ')
        nombre = self.pedirdato('Introduzca el nombre: ')
        fecha = Ejercicio4.pedirdato('Introduzca la fecha de nacimiento, (Formato recomendado yyyy-mm-dd): ')
        direccion = self.pedirdato('Introduzca la dirección: ')
        password = Ejercicio4.pedirdato('Introduzca la contraseña: ')
        clave = len(self.tabla)

        self.tabla.update(({clave: {'apellidos': apellidos, 'nombre': nombre, 'fecha': fecha,
                                    'direccion': direccion, 'password': password}}))
        cuenta = len(self.tabla)
        print('')

        if cuenta > clave:
            print('## Usuario añadido correctamente')
        else:
            print('## Error indeterminado al crear el usuario')

        self.pulseintro()

    def buscardatos(self):
        print('')
        contador = 0
        print('### Buscar datos ###')
        dato = self.pedirdato('Introduzca nombre o apellido a buscar: ')
        print('')
        for registro in self.tabla:
            fila = self.tabla.get(registro)
            nombre = fila.get('nombre')
            apellidos = fila.get('apellidos')

            if nombre == dato or apellidos == dato:
                contador += 1
                print('### Datos encontrados ###')
                print('Nombre: ', nombre)
                print('Apellidos: ', apellidos)
                print('Fecha de Nacimiento: ', fila.get('fecha'))
                print('Dirección: ', fila.get('direccion'))
                print('Password: ', fila.get('password'))
                print('')

        if contador == 0:
            print('## Revise lo escrito, ningún usuario encontrado')
        print('')
        self.pulseintro()

    def agregardatosacsv(self):
        titulo_columnas = ['apellidos', 'nombre', 'fecha', 'direccion', 'password']
        cuenteo: int = 0
        nombreficherocsv: str = 'diccionarioimportado.csv'
        print('')
        print('### Agregar datos a un CSV ###')
        print('Fichero destino: ', nombreficherocsv)
        print('')

        with open(nombreficherocsv, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=titulo_columnas)
            writer.writeheader()
            # writer.writerows(self.tabla)
            csvfile.close()

        with open('diccionarioimportado.csv', 'a') as csvfileappend:
            w = csv.writer(csvfileappend)
            for registro in self.tabla:
                fila = self.tabla.get(registro)
                nombre: str = fila.get('nombre')
                apellidos: object = fila.get('apellidos')
                fecha: str = fila.get('fecha')
                direccion: str = fila.get('direccion')
                password: str = fila.get('password')
                w.writerow([apellidos, nombre, fecha, direccion, password])
                cuenteo += 1
            csvfileappend.close()
        print('## Proceso acabado, registros añadidos: ', cuenteo)
        print('')
        self.pulseintro()

    def recuperardatos(self):
        # nombreficherocsv: str = 'diccionarioimportado.csv'
        print('')
        print('### Recuperar datos de un CSV ###')
        print('')
        nombreficherocsv = input('Escribe la ruta del fichero')
        print('')
        try:
            with open(nombreficherocsv, mode='r') as file:
                csvfile = csv.DictReader(file)

                for lines in csvfile:
                    nombre: str = lines.get('nombre')
                    apellidos: str = lines.get('apellidos')
                    fecha: str = lines.get('fecha')
                    direccion: str = lines.get('direccion')
                    password: str = lines.get('password')
                    print('>>> Añadiendo usuario ')
                    print('Nombre: ', nombre)
                    print('Apellidos: ', apellidos)
                    print('Fecha de Nacimiento: ', fecha)
                    print('Dirección: ', direccion)
                    print('Password: ', password)
                    print('')

                    clave = len(self.tabla)
                    self.tabla.update(({
                        clave: {'apellidos': apellidos, 'nombre': nombre, 'fecha': fecha, 'direccion': direccion,
                                'password': password}}))
                    cuenta = len(self.tabla)

                    if cuenta > clave:
                        print('## Usuario añadido correctamente')
                    else:
                        print('## Error indeterminado al añadir el usuario')
                    print('')
        except FileNotFoundError:
            print('Fichero indicado no encontrado.')
        print('')
        self.pulseintro()


if __name__ == '__main__':
    foo = Ejercicio4()
    foo.comenzar()
