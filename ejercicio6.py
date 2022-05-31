import csv
from modulos_apoyo.tools import Tools
from modulos_apoyo.pgsql import Sqlcommand

# Prerequisitos
# sudo apt install python3-pip
# pip uninstall psycopg2
# pip install psycopg2-binary


class Ejercicio6:

    def __init__(self):
        self.nombreclase = 'Ejercicio6'
        self.conn = None

    def comenzar(self):
        Tools.titulo(self.nombreclase)
        print('')
        print('1) Solicitar datos para conectarse a la BD local')
        print('2) Conexión con mi "configuración"')
        print('0) Salir')
        print('')
        while True:
            num = Tools.pedirdato('Escriba el número de la opción: ')
            print('')
            if num == "1":
                self.conn = Sqlcommand.conexionpostgresqlsolicitadatos()
                if self.conn is not None:
                    self.menuopciones()
                break
            elif num == "2":
                self.conn = Sqlcommand.conexionpostgresql()
                if self.conn is not None:
                    self.menuopciones()
                break
            elif num == "0":
                print('Opción 0, salimos')
                break
            else:
                print('Opción erronea, vuelva a probar')

    def menuopciones(self):
        try:
            Tools.titulo('Menu de opciones')
            while True:
                self.menuinicial()
                opcionmenu = Tools.pedirdato("Elija número de opción: ")

                if opcionmenu == "0":
                    print('Opción 0, salimos')
                    break
                elif opcionmenu == "1":
                    self.moduloclientesproveedores()
                elif opcionmenu == "2":
                    self.modulomodificarclienteproveedor()
                else:
                    print('Opción erronea, vuelva a probar')

        except (Exception,):
            print('Se ha generado una excepcion')

    @staticmethod
    def menuinicial():
        print('')
        print('1) Módulo Clientes/Proveedores: Importación CSV')
        print('2) Módulo Clientes/Proveedores: Mostrar y Modificar')
        print('0) Salir')
        print('')

    def moduloclientesproveedores(self):
        print('')
        Tools.titulo('Importación CSV de Clientes/Proveedores')
        print('')
        rutaficherocsv = Tools.pedirdato('Escribe nombre fichero: ')
        cuentaclientesactualizados = 0
        cuentaclientesinsertados = 0

        print('')
        try:
            with open(rutaficherocsv, mode='r') as file:
                csvfile = csv.DictReader(file)

                for lines in csvfile:
                    nombre: str = lines.get('nombre del cliente')
                    contacto: str = lines.get('persona de contacto')
                    direccion: str = lines.get('direccion')
                    telf: str = lines.get('telefono')
                    email: str = lines.get('e-mail')
                    web: str = lines.get('pagina web')
                    poblacion: str = lines.get('poblacion')
                    cp: str = lines.get('codigo postal')
                    tipo: str = lines.get('tipo')
                    print('>>> Datos leidos <<<')
                    print('Nombre: ', nombre)
                    print('Contacto: ', contacto)
                    print('Direccion: ', direccion)
                    print('Telf: ', telf)
                    print('e-mail: ', email)
                    print('Web: ', web)
                    print('Poblacion: ', poblacion)
                    print('cp: ', cp)
                    print('Tipo: ', tipo)
                    print('## Comprobamos si el cliente ya existe...')
                    datoscliente = [nombre, contacto, direccion, telf, email, web, poblacion, cp, tipo]
                    if Sqlcommand.existenombrecliente(self.conn, nombre) is True:
                        print('El cliente existe, actualizamos >>')
                        idcliente = Sqlcommand.dameidsegunelnombredecliente(self.conn, nombre)
                        datoscliente.append(idcliente)
                        resultadoact = Sqlcommand.actualizarclientedesdecsv(self.conn, datoscliente)
                        cuentaclientesactualizados += resultadoact

                    else:
                        print('El cliente NO existe, insertamos >>')
                        resultadoinsert = Sqlcommand.insertarclientedesdecsv(self.conn, datoscliente)
                        cuentaclientesinsertados += resultadoinsert
                        idcliente = Sqlcommand.dameidsegunelnombredecliente(self.conn, nombre)
                        datoscliente.append(idcliente)
                        Sqlcommand.insertarloginandpassword(self.conn, datoscliente)
                    print('')
            file.close()
            print('')
            print('## Registros actualizados: ', cuentaclientesactualizados)
            print('## Registros Insertados: ', cuentaclientesinsertados)
            print('')
        except FileNotFoundError:
            print('Fichero indicado no encontrado')
            print('')
        Tools.pulseintro()

    def modulomodificarclienteproveedor(self):
        Sqlcommand.consultaclientes(self.conn)
        respuesta = Tools.pedirdato('¿Quiere modificar algún registro? (y/n): ')
        if respuesta == 'y' or respuesta == 'Y':
            self.modificarcliente()
        else:
            print('Ha elegido "NO" o una opción incorrecta')
        Tools.pulseintro()
        pass

    def modificarcliente(self):
        codelegido = Tools.pedirdato('Indique el ID del registro a modificar: ')
        if codelegido.isdigit():
            if Sqlcommand.existecliente(self.conn, codelegido) is True:
                nombre = Tools.pedirdato('Introduzca el nuevo nombre: ')
                calle = Tools.pedirdato('Introduzca la nueva calle: ')
                cp = Tools.pedirdato('Introduzca el nuevo C.P.: ')
                ciudad = Tools.pedirdato('Introduzca la nueva ciudad: ')
                telf = Tools.pedirdato('Introduzca el nuevo telefono: ')
                tipo = Tools.pedirdato('Introduzca el nuevo tipo: ')
                email = Tools.pedirdato('Introduzca el nuevo email: ')
                web = Tools.pedirdato('Introduzca el nuevo website: ')
                Sqlcommand.actualizarregistroclientes(self.conn, [codelegido, nombre, calle, cp, ciudad, telf, tipo,
                                                                  email, web])

            else:
                print('El código de cliente no existe')
        else:
            print('El código ha de ser numérico')


if __name__ == '__main__':
    foo = Ejercicio6()
    foo.comenzar()
