import psycopg2
import csv


# Prerequisitos
# sudo apt install python3-pip
# pip uninstall psycopg2
# pip install psycopg2-binary


class Ejercicio5:
    def __init__(self):
        self.nombreclase = 'Ejercicio5'
        self.conn = None

    @staticmethod
    def conexionpostgresql():
        conn = None
        try:
            conn = psycopg2.connect(host="localhost", database="segun", user="odoo", password="odoo")
        except (Exception, psycopg2.DatabaseError):
            print('')
            print('Error de conexión, revise los datos introducidos')
        except (Exception,):
            print('')
            print('Se ha generado una excepcion')
        return conn

    def conexionpostgresqlsolicitadatos(self):
        conn = None
        try:
            database = self.pedirdato('Introduce database: ')
            user = self.pedirdato('Introduce user: ')
            password = self.pedirdato('Introduce password: ')
            print('')
            conn = psycopg2.connect(host="localhost", database=database, user=user, password=password)
        except (Exception, psycopg2.DatabaseError):
            print('')
            print('Error de conexión, revise los datos introducidos')
        except (Exception,):
            print('')
            print('Se ha generado una excepcion')
        return conn

    def comenzar(self):
        self.presentacion()
        print('')
        print('1) Solicitar datos para conectarse a la BD local')
        print('2) Conexión con mi "configuración"')
        print('0) Salir')
        print('')
        while True:
            num = input('Escriba el número de la opción: ')
            print('')
            if num == "1":
                self.conn = self.conexionpostgresqlsolicitadatos()
                if self.conn is not None:
                    self.conn.commit()
                    self.menuopciones()
                break
            elif num == "2":
                self.conn = Ejercicio5.conexionpostgresql()
                if self.conn is not None:
                    self.conn.commit()
                    self.menuopciones()
                break
            elif num == "0":
                print('Opción 0, salimos')
                break
            else:
                print('Opción erronea, vuelva a probar')

    def menuopciones(self):
        try:
            Ejercicio5.titulo('Menu de opciones')
            while True:
                self.menuinicial()
                opcionmenu = Ejercicio5.pedirdato("Elija número de opción: ")

                if opcionmenu == "0":
                    print('Opción 0, salimos')
                    break
                elif opcionmenu == "1":
                    self.consultaproductos()
                elif opcionmenu == "2":
                    self.mostrardetallesproducto()
                elif opcionmenu == "3":
                    self.agregardatosacsv()
                else:
                    print('Opción erronea, vuelva a probar')

        except (Exception,):
            print('Se ha generado una excepcion')

    def presentacion(self):
        print('##################')
        print(self.nombreclase)
        print('##################')

    @staticmethod
    def titulo(msg: str):
        print('##################')
        print(msg)
        print('##################')

    @staticmethod
    def menuinicial():
        print('')
        print('1) Mostrar listado de productos')
        print('2) Mostrar los detalles de un producto')
        print('3) Generar fichero CSV')
        print('0) Salir')
        print('')

    @staticmethod
    def pedirdato(mensaje):
        leido = input(mensaje)
        return leido

    @staticmethod
    def pulseintro():
        input("Presione INTRO para continuar...")

    def consultaproductos(self):
        cur = None
        print('')
        Ejercicio5.titulo('Listado de productos')
        print('')
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT * '
                        'FROM product_template '
                        "WHERE type like 'product' "
                        'AND has_configurable_attributes = false '
                        'ORDER BY id')
            listaproductos = cur.fetchall()
            print('%5s%30s%12s%12s%12s%20s%10s' % ('ID', 'NOMBRE', 'TIPO', 'ID_CATEG', 'PRECIO',
                                                   'DEFAULT_CODE', 'PESO'))
            for fila in listaproductos:
                print('%5s%30s%12s%12s%12s%20s%10s' % (fila[0], fila[2], fila[8], fila[9],
                                                       fila[10], fila[20], fila[12]
                                                       ))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        except (Exception,):
            print('Se ha generado una excepcion')
        finally:
            if cur is not None:
                cur.close()
        print('')
        self.pulseintro()

    def mostrardetallesproducto(self):
        print('')
        Ejercicio5.titulo('Detalles de producto')
        print('')
        cur = None
        try:
            idproducto: str = Ejercicio5.pedirdato('Introduce el número de ID del producto: ')

            if idproducto.isdigit():

                cur = self.conn.cursor()
                cur.execute('SELECT p.id, p.name, p.default_code, p.description '
                            'FROM product_template p '
                            "WHERE type like 'product' "
                            'AND p.has_configurable_attributes = false '
                            'AND p.id = ' + idproducto)
                producto = cur.fetchone()
                if producto is not None:
                    print('ID: ', producto[0])
                    print('Nombre: ', producto[1])
                    print('Default Code: ', producto[2])
                    print('Descripción: ', producto[3])
                    sto = self.consultarstock(str(producto[0]))
                    if sto is None:
                        sto = '0'
                    print('Stock: ', sto)
                else:
                    print('Sin resultados')
            else:
                print('El código ha de ser un número entero')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        except (Exception,):
            print('Se ha generado una excepcion.')
        finally:
            if cur is not None:
                cur.close()
        print('')
        self.pulseintro()

    def consultarstock(self, idcod):
        query = 'SELECT sum(sq.inventory_diff_quantity) ' \
                'FROM product_template pt ' \
                'INNER JOIN product_product pp on pp.default_code = pt.default_code ' \
                'INNER JOIN stock_quant sq ON sq.product_id = pp.id ' \
                'WHERE pt.id = ' + idcod
        cur = None
        resultado = None

        try:
            cur = self.conn.cursor()
            cur.execute(query)
            resultado = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        except (Exception,):
            print('Se ha generado una excepcion')
        finally:
            if cur is not None:
                cur.close()
                return resultado[0]
        return resultado[0]

    def agregardatosacsv(self):
        titulo_columnas = ['ID', 'Nombre', 'Default_code', 'Descripción', 'Stock']
        cuenteo: int = 0
        nombreficherocsv: str = 'ProductosOdoo.csv'
        querystring = 'SELECT p.id, p.name, p.default_code, p.description ' \
                      'FROM product_template p ' \
                      'WHERE type like \'product\' ' \
                      'AND p.has_configurable_attributes = false ' \
                      'ORDER BY p.description'
        print('')
        print('### Generar fichero CSV ###')
        print('Fichero destino: ', nombreficherocsv)
        print('')

        with open(nombreficherocsv, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=titulo_columnas)
            writer.writeheader()
            # writer.writerows(self.tabla)
            csvfile.close()

        with open(nombreficherocsv, 'a') as csvfileappend:
            w = csv.writer(csvfileappend)
            listaproductos = self.consultaany(querystring)

            for producto in listaproductos:
                idcod: str = producto[0]
                nombre: str = producto[1]
                defaultcode: str = producto[2]
                descripcion: str = producto[3]
                stock: str = producto[4]
                w.writerow([idcod, nombre, defaultcode, descripcion, stock])
                cuenteo += 1

            csvfileappend.close()
        print('## Proceso acabado, registros añadidos: ', cuenteo)
        print('')
        self.pulseintro()

    def consultaany(self, querystring: str):
        cur = None
        listaproductos = list()
        try:
            cur = self.conn.cursor()
            cur.execute(querystring)
            resultadoquery = cur.fetchall()
            for producto in resultadoquery:
                idcod: str = producto[0]
                nombre: str = producto[1]
                defaultcode: str = producto[2]
                descripcion: str = producto[3]
                stock: str = self.consultarstock(str(producto[0]))
                if stock is None:
                    stock = '0'
                listaproductos.append([idcod, nombre, defaultcode, descripcion, stock])

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        except (Exception,):
            print('Se ha generado una excepcion')
        finally:
            if cur is not None:
                cur.close()
                return listaproductos


if __name__ == '__main__':
    foo = Ejercicio5()
    foo.comenzar()
