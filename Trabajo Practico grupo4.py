#Grupo nro°4 Integrantes:
#Decroce LEonardo
#Gomez melisa 

import sqlite3 as sql  #Importamos librería para poder usar SQL y bases de datos.
import datetime #Importamos la librería que nos permite el uso de elementos de tipo fecha.

#Creación de clase programa, para luego poder ejecutarlo como un objeto.
class programa():
    #Metodo menú,que llama funciones externas para poder realizar las diferentes órdenes.
    def menu(self):
        bandera = True #Definición de una bandera, para que el bucle WHILE se repita infinitas veces hasta que por orden propia lo detengamos.
        while bandera == True:
            #Opciones que nos brinda el menú.
            print("Menú de opciones:")
            print("1-Cargar monopatín.")
            print("2-Modificar un registro.")
            print("3-Borrar un registro.")
            print("4-Cargar disponibilidad.")
            print("5-Listar productos.")
            print("6-Crear nueva tabla personalizada. Ingresar registros a la tabla.")
            print("7-Aumentar precio.")
            print("8-Mostrar todos los registros.(Debe usarse la opción 7 previamente)")
            print("0-Salir del programa.")
            #Carga de la variable "opcion", que nos permite actuar como el operador para la estructura SWITCH/CASE(creada por Ifs).
            opcion = int(input("Seleccione una opción:\n")) 
            #Bucle WHILE para controlar las opciones seleccionables. Si no cumple la condición, solicita la carga de la variable "opcion" nuevamente.
            while opcion < 0 or opcion > 8:
                opcion = int(input("Opción inválida, vuelva a intentarlo:\n"))

            
            if opcion == 1: #Opción 1- Cargamos 3 variables y las pasamos como parámetros en la función para cargar un registro completo para la tabla "Monopatines", en nuestra base de datos.
                marca = str(input("Inserte el nombre de la marca:"))
                precio = float(input("Inserte el precio del producto:"))
                cantidad = int(input("Inserte la cantidad en stock del producto:"))
                insertarRegistro(marca,precio,cantidad)

            elif opcion == 2: #Opción 2- Solicitamos un Id como variable y un nuevo precio. Comparamos el Id con el que se encuentra en la base de Datos.Si se encuentra, reemplaza el precio anterior por el nuevo.
                nuevoId = int(input("Ingrese el id del producto que desea modificar:\n"))
                nuevoPrecio = float(input("Ingrese el nuevo valor del producto seleccionado:\n"))
                actualizarPrecio(nuevoPrecio, nuevoId)

            elif opcion == 3: #Opción 3- Borra un registro en base a un Id que le pasamos por consola.
                nombreTabla = str(input("Ingrese el nombre de la tabla en la que desea borrar un registro:\n"))
                nuevoId = int(input("Ingrese el id del producto que desea borrar:\n"))
                borrarMonopatin(nombreTabla,nuevoId)

            elif opcion == 4: #Opción 4- Pasamos por consola una variable con la marca, si hay una parecida o igual en la BD, aumentamos el stock en 1.
                nombreMarca = str(input("Ingrese el nombre de la marca a la que desa aumentar el stock:"))
                cargarDisponibilidad(nombreMarca)

            elif opcion == 5: #Opción 5- Permite visualizar una de las tres tablas creadas. Es necesario escribir el nombre de la tabla para que se muetren en pantalla.
                nombreTabla = str(input("Ingrese Monopatines para ver la tabla estandar o Monopatin para ver la tabla personalizada.\nIngrese HistoricoPrecios para ver la tabla con el aumento de precio.\n"))
                if nombreTabla != "Monopatines" and nombreTabla != "Monopatin" and nombreTabla != "HistoricoPrecios":
                    nombreTabla = str(input("Nombre de tabla inválido. Vuelva a ingresar el nombre de la tabla:"))
                leerTabla(nombreTabla)

            elif opcion == 6: #Opción 6- Crea un con nuevas columnas para una nueva tabla llamada "Monopatin".
                print("Ingrese los datos de un producto a la nueva tabla.")
                modelo = str(input("Ingrese el modelo:"))
                marca = str(input("Ingrese la marca:"))
                potencia = str(input("Ingrese la potencia:"))
                precio = int(input("Ingrese el precio:"))
                color = str(input("Ingrese el color:"))
                año = int(input("Ingrese el año de ingreso del producto:"))
                mes = int(input("Ingrese el mes de ingreso del producto:"))
                dia = int(input("Ingrese el día de ingreso del producto:"))
                fechaUltimoPrecio = datetime.datetime(año, mes, dia)
                cargarRegistroNuevaTabla(modelo,marca,potencia,precio,color,fechaUltimoPrecio)

            elif opcion == 7: # Opción 7- Colona todos los registros de la tabla utilizada en la opción nº6 y crea una nueva tabla llamada "HistoricoPrecios" y le regarga el precio en 0.23%.
                clonarTabla()
                actualizarDolar()
            
            #LA OPCIÓN Nº8 REQUIERE DE FORMA OBLIGATORIA HABER UTILIZADO LA OPCIÓN Nº7.DE LO CONTRARIO NOS MOSTRARÁ UNA LISTA VACÍA.
            elif opcion == 8: # Opción 8- Creamos variables para año, mes y día, que luego utilizamos para pasar como parámetro de tipo fecha en la función. Nos muestra los registros que tengan una fecha anterior a la que fue pasada como parámetro.
                año = int(input("Ingrese el año de ingreso del producto:"))
                mes = int(input("Ingrese el mes de ingreso del producto:"))
                dia = int(input("Ingrese el día de ingreso del producto:"))
                fecha = datetime.datetime(año, mes, dia)
                filtrarPorFecha(fecha)

            else: #Funciona solo con el número 0 al pasarlo por consola. BORRA las tablas creadas y cambia la bandera lo que permite romper con el loop infinito del menú.
                bandera = False
                tabla1= "Monopatines"
                tabla2= "Monopatin"
                tabla3= "HistoricoPrecios"
                borrarTabla(tabla1)
                borrarTabla(tabla2)
                borrarTabla(tabla3)
                print("Saliendo del programa.")


def crearBD(): #Crea una nueva base de datos llamada "Monopatines".
    conn = sql.connect("Monopatines.db")
    conn.commit()
    conn.close()

def crearTabla(): #Crea una tabla llamada "Monopatines" con cuatro columnas.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE Monopatines (
            id INTEGER NOT NULL PRIMARY KEY,
            marca text UNIQUE,
            precio integer,
            cantidad integer
            )"""
        )
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()

def insertarRegistro(marca, precio, cantidad): #Inserta los datos de cada uno de los parámetros en una columna específica de la tabla "Monopatines".
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        instruccion = f"INSERT INTO Monopatines (marca,precio,cantidad) VALUES ('{marca}' , {precio} , {cantidad})"
        cursor.execute(instruccion)
        conn.commit()
    except:
        print("ERROR.")
    finally:        
        conn.close()

def leerTabla(nombreTabla): #Lee una tabla y la muestra por pantalla en base al nombre que le pasemos por consola.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM '{nombreTabla}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()
        print(datos)

def borrarTabla(tabla): #Borra definitivamente una tabla, en base al nombre que le pasemos por consola.
    try:
        conn = sql.connect('Monopatines.db')
        instruccion = f"DROP TABLE '{tabla}'"
        conn.execute(instruccion)
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()
        print("Tabla borrada.")

def actualizarPrecio(nuevoPrecio,nuevoId): #Si encuentra una similitud de ID, nos permite modificar el precio de un producto en el regisro que posee ese ID.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        instruccion = f"UPDATE Monopatines SET precio={nuevoPrecio} WHERE id={nuevoId}"
        cursor.execute(instruccion)
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()

def borrarMonopatin(nombreTabla,nuevoId): #Borra un registro en particular de la tabla selecionada.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        instruction= f"DELETE from '{nombreTabla}' where id={nuevoId}"
        cursor.execute(instruction)
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()

def cargarDisponibilidad(nombreMarca): #Incrementa la cantidad del stock en 1 del monopatín que pasemos la "marca" por consola.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        instruccion = f"UPDATE Monopatines SET cantidad=cantidad+1 WHERE marca like '{nombreMarca}'"
        cursor.execute(instruccion)
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()

def nuevaTabla(): #Crea una nueva tabla "Monopatin", con más columnas que la tabla anterior.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE Monopatin (
            id_mono integer NOT NULL PRIMARY KEY,
            modelo varchar(30),
            marca varchar(30),
            potencia varchar(30),
            precio integer,
            color varchar(30),
            fechaUltimoPrecio datetime
            )""")
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()

def cargarRegistroNuevaTabla(modelo,marca,potencia,precio,color,fechaUltimoPrecio): #Crea un registro y almacena los datos de los parámetros en la columna correspondiente.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        instruccion = f"INSERT INTO Monopatin (modelo,marca,potencia,precio,color,fechaUltimoPrecio) VALUES ('{modelo}', '{marca}' , '{potencia}' , {precio} , '{color}' , '{fechaUltimoPrecio}')"
        cursor.execute(instruccion)
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()

def clonarTabla(): #Clona todas las columnas de la tabla "Monopatin" y crea una nueva tabla con dichas columnas.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE HistoricoPrecios AS SELECT * FROM Monopatin WHERE 0""")
        cursor.execute("""INSERT INTO HistoricoPrecios SELECT * FROM Monopatin""")
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()

def actualizarDolar(): #Actualiza el precio incrementándolo en 0.23% del total anterior.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        instruccion = f"UPDATE HistoricoPrecios SET precio=precio*1.23"
        cursor.execute(instruccion)
        conn.commit()
    except:
        print("Para ver la tabla insertar 'HistoricoPrecios' en la opción Nº 5.")
    finally:
        conn.close()

def filtrarPorFecha(fecha): #Hace una comparación de fechas y nos muestra los registro que posean una fecha anterior.
    try:
        conn = sql.connect("Monopatines.db")
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM HistoricoPrecios WHERE fechaUltimoPrecio < '{fecha}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        conn.commit()
    except:
        print("ERROR.")
    finally:
        conn.close()
        print(datos)

#Creamos un objeto, de clase "programa".
Ejecutar = programa()
#Creamos la base de datos.
crearBD()
#Creamos la tabla "Monopatines".
crearTabla()
#Creamos la tabla "Monopatin".
nuevaTabla()
#Ejecutamos el método "menu" de la clase "programa" a través del objero "Ejecutar".
Ejecutar.menu()