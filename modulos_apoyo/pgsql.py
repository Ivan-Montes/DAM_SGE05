import psycopg2
from modulos_apoyo.tools import Tools


class Sqlcommand:

    def __init__(self):
        self.name = "Sqlcommand"

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

    @staticmethod
    def conexionpostgresqlsolicitadatos():
        conn = None
        try:
            database = Tools.pedirdato('Introduce database: ')
            user = Tools.pedirdato('Introduce user: ')
            password = Tools.pedirdato('Introduce password: ')
            print('')
            conn = psycopg2.connect(host="localhost", database=database, user=user, password=password)
        except (Exception, psycopg2.DatabaseError):
            print('')
            print('Error de conexión, revise los datos introducidos')
        except (Exception,):
            print('')
            print('Se ha generado una excepcion')
        return conn

    @staticmethod
    def consultalientes(conn):
        cur = None
        print('')
        try:
            cur = conn.cursor()
            cur.execute('SELECT rp.id, rp.name, rp.street, rp.zip, rp.city, rp.phone, rp.type, rp.email, rp.website '
                        'FROM res_partner rp '
                        'ORDER BY rp.id')
            listaproductos = cur.fetchall()
            print('%5s%35s%40s%10s%25s%25s%15s%35s%35s' % ('ID', 'NOMBRE', 'CALLE', 'C.P.', 'CIUDAD',
                                                           'TELÉFONO', 'TIPO', 'EMAIL', 'WEBSITE'))
            for fila in listaproductos:
                print('%5s%35s%40s%10s%25s%25s%15s%35s%35s' % (fila[0], fila[1], fila[2], fila[3],
                                                               fila[4], fila[5], fila[6], fila[7], fila[8]
                                                               ))
            cur.close()
        except (Exception, psycopg2.Error) as error:
            print(error)
        except (Exception,):
            print('Se ha generado una excepcion')
        finally:
            if cur is not None:
                cur.close()
        print('')

    @staticmethod
    def existeidcliente(conn, idcliente):
        querystring = 'SELECT count(*) ' \
                      'FROM res_partner rp ' \
                      'WHERE rp.id = ' + str(idcliente)
        cur = None
        result = False

        try:
            cur = conn.cursor()
            cur.execute(querystring)
            resultquery = cur.fetchone()
            if resultquery[0] > 0:
                result = True
        except psycopg2.Error:
            print('Excepción psycop2 en existenombrecliente')
        except (Exception,):
            print('Excepcion en existenombrecliente')
        if cur is not None:
            cur.close()
        return result

    @staticmethod
    def existenombrecliente(conn, nombrecliente: str):
        querystring = 'SELECT count(*) ' \
                      'FROM res_partner rp ' \
                      'WHERE rp.name like \'' + nombrecliente + '\''
        cur = None
        result = False

        try:
            cur = conn.cursor()
            cur.execute(querystring)
            resultquery = cur.fetchone()
            if resultquery[0] > 0:
                result = True
        except psycopg2.Error:
            print('Excepción psycop2 en SqlCommand existenombrecliente')
        except (Exception,):
            print('Excepcion en SqlCommand.existenombrecliente')
        if cur is not None:
            cur.close()
        return result

    @staticmethod
    def dameidsegunelnombredecliente(conn, nombrecliente: str):
        querystring = 'SELECT rp.id ' \
                      'FROM res_partner rp ' \
                      'WHERE rp.name like \'' + nombrecliente + '\''
        cur = None
        resultquery = None

        try:
            cur = conn.cursor()
            cur.execute(querystring)
            resultquery = cur.fetchone()
        except psycopg2.Error:
            print('Excepción psycop2 en dameidsegunelnombredecliente')
        except (Exception,):
            print('Excepcion en dameidsegunelnombredecliente')
        if cur is not None:
            cur.close()
        return resultquery[0]

    @staticmethod
    def existeidusuarioenresuser(conn, idcliente):
        querystring = 'SELECT count(*) ' \
                      'FROM res_users rp ' \
                      'WHERE rp.partner_id = ' + str(idcliente)
        cur = None
        result = False

        try:
            cur = conn.cursor()
            cur.execute(querystring)
            resultquery = cur.fetchone()
            if resultquery[0] > 0:
                result = True
        except psycopg2.Error:
            print('Excepción psycop2 en sql command existenombrecliente')
        except (Exception,):
            print('Excepcion en sql command existenombrecliente')
        if cur is not None:
            cur.close()
        return result

    @staticmethod
    def actualizarclientedesdecsv(conn, datoscliente):
        cur = None
        cuenta = 0
        querystring = 'UPDATE res_partner ' \
                      'SET name = \'' + datoscliente[0] + '\', ' \
                                                          'additional_info = \'' + datoscliente[1] + '\', ' \
                                                                                                     'street = \'' + \
                      datoscliente[2] + '\', ' \
                                        'phone = \'' + datoscliente[3] + '\', ' \
                      'email = \'' + datoscliente[4] + '\', ' \
                      'website = \'' + \
                      datoscliente[5] + '\', ' \
                      'city = \'' + datoscliente[6] + '\', ' \
                      'zip = \'' + datoscliente[7] + '\', ' \
                      'type = \'' + \
                      datoscliente[8] + '\' ' \
                      'WHERE id = ' + str(datoscliente[9])
        try:
            cur = conn.cursor()
            cur.execute(querystring)
            conn.commit()
            cuenta = cur.rowcount

        except (Exception, psycopg2.Error) as error:
            print("Error en la actualización", error)
        except (Exception,):
            print('Excepción al actualizar registros')
        if cur is not None:
            cur.close()
        return cuenta

    @staticmethod
    def insertarclientedesdecsv(conn, datoscliente):
        cur = None
        cuenta = 0
        querystring = 'INSERT INTO res_partner' \
                      '(name, additional_info, street, phone, email, website, city, ' \
                      'zip, type, active, display_name, lang, create_date) ' \
                      'VALUES' \
                      '(\'' + datoscliente[0] + '\',\'' + datoscliente[1] + '\',\'' + datoscliente[2] + '\',' \
                                                                                                        '\'' + \
                      datoscliente[3] + '\',\'' + datoscliente[4] + '\',\'' + datoscliente[5] + '\',' \
                                                                                                '\'' + datoscliente[
                          6] + '\',\'' + datoscliente[7] + '\',\'' + datoscliente[8] + '\',' \
                                                                                       'true, \'' + datoscliente[
                          0] + '\',\'es_ES\', now() )'

        try:
            cur = conn.cursor()
            cur.execute(querystring)
            conn.commit()
            cuenta = cur.rowcount

        except (Exception, psycopg2.Error) as error:
            print("Error en la inserción", error)
        except (Exception,):
            print('Excepción al insertar registros')
        if cur is not None:
            cur.close()
        return cuenta

    @staticmethod
    def insertarloginandpassword(conn, datoscliente):
        login = Tools.crearloginusuario(datoscliente[0])
        passwd = Tools.crearpassword(datoscliente[0])
        idcliente = str(datoscliente[9])
        cur = None
        cuenta = 0
        sqlstring = 'INSERT INTO res_users ' \
                    '(partner_id, active, login, password,company_id, ' \
                    'create_date, write_date, share, notification_type)' \
                    'VALUES' \
                    '(' + idcliente + ', true,\'' + login + '\',\'' + passwd + '\', 1,' \
                    'now(), now(), false,\'email\')'

        try:
            cur = conn.cursor()
            cur.execute(sqlstring)
            conn.commit()
            cuenta = cur.rowcount
        except(Exception, psycopg2.Error)as error:
            print("Error psycopg2 en insertarloginandpassword", error)
        except(Exception,):
            print("Error en insertarloginandpassword")
        if cur is not None:
            cur.close()
        return cuenta

    @staticmethod
    def consultaclientes(conn):
        cur = None
        print('')
        Tools.titulo('Listado de Clientes/Proveedores')
        print('')
        try:
            cur = conn.cursor()
            cur.execute('SELECT rp.id, rp.name, rp.street, rp.zip, rp.city, rp.phone, rp.type, rp.email, rp.website '
                        'FROM res_partner rp '
                        'ORDER BY rp.id')
            listaproductos = cur.fetchall()
            print('%5s%35s%40s%10s%25s%25s%15s%35s%35s' % ('ID', 'NOMBRE', 'CALLE', 'C.P.', 'CIUDAD',
                                                           'TELÉFONO', 'TIPO', 'EMAIL', 'WEBSITE'))
            for fila in listaproductos:
                print('%5s%35s%40s%10s%25s%25s%15s%35s%35s' % (fila[0], fila[1], fila[2], fila[3],
                                                               fila[4], fila[5], fila[6], fila[7], fila[8]
                                                               ))
            cur.close()
        except (Exception, psycopg2.Error) as error:
            print(error)
        except (Exception,):
            print('Se ha generado una excepcion')
        finally:
            if cur is not None:
                cur.close()
        print('')

    @staticmethod
    def existecliente(conn, codcliente: str):
        cur = None
        querystring = 'SELECT count(rp.id) FROM res_partner rp WHERE rp.id = ' + codcliente
        resultado = False

        try:
            cur = conn.cursor()
            cur.execute(querystring)
            resultadoquery = cur.fetchone()
            cur.close()

            if resultadoquery[0] > 0:
                resultado = True

        except (Exception, psycopg2.Error) as error:
            print(error)

        except (Exception,):
            print('Se ha generado una excepcion.')

        if cur is not None:
            cur.close()

        return resultado

    @staticmethod
    def actualizarregistroclientes(conn, datoscliente):
        cur = None
        querystring = 'UPDATE res_partner ' \
                      'SET name = \'' + datoscliente[1] + '\', ' \
                      'street = \'' + datoscliente[2] + '\', ' \
                      'zip = \'' + datoscliente[3] + '\', ' \
                      'city = \'' + datoscliente[4] + '\', ' \
                      'phone = \'' + datoscliente[5] + '\', ' \
                      'type = \'' + datoscliente[6] + '\', ' \
                      'email = \'' + datoscliente[7] + '\', ' \
                      'website = \'' + datoscliente[8] + '\' ' \
                      'WHERE id = ' + datoscliente[0]
        try:
            cur = conn.cursor()
            cur.execute(querystring)
            conn.commit()
            cuenta = cur.rowcount
            print('')
            print('## Registros actualizados: ', cuenta)
            print('')

        except (Exception, psycopg2.Error) as error:
            print("Error en la actualización", error)
        except (Exception,):
            print('Excepción al actualizar registros')
        if cur is not None:
            cur.close()
