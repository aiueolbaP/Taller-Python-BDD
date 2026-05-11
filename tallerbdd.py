# Función consultar registros
# Fernando Karolys, Deivy Molina, Pablo Flores


def consultar_registro(conexion):
    #Inicio
    try:
        print("\n\t\tCONSULTA CURSOS:\n")  
        # 1.Cree una variable para la cadena de consulta SQL.
        SQL_QUERY = """
        SELECT IDCurso,NombreCurso,Descripcion,PrecioxHora,TipoCurso
        FROM Cursos
        """
        cursor = conexion.cursor()
        cursor.execute(SQL_QUERY)
        records = cursor.fetchall()
        for r in records:
            print(f"{r.IDCurso}\t{r.NombreCurso} \t {r.Descripcion}\t{r.PrecioxHora} \t {r.TipoCurso}")
        
        
    
    except Exception as e:
        print("\n \t Ocurrió un error al consultar a SQL Server: \n\n", e)
    


# Función insertar registros
def insertar_registro(conexion):
    #Crear Cursor
    try:

        micursor = conexion.cursor()
        
        SENTENCIA_SQL = """
        INSERT INTO Cursos
        (IDCurso,NombreCurso,Descripcion,PrecioxHora,TipoCurso)
        VALUES(?,?,?,?,?)
        """
          
        print("\n\t\tINSERTAR NUEVO Curso:\n")  
        ## Ingreso de Informacion
        l_IDCurso = int(input("Ingrese ID del Curso: \t"))
        l_NombreCurso = input("Ingrese Nombre del Curso: \t")
        l_Descripcion = input("Ingrese Descripcion del curso:\t")
        l_PrecioxHora = float(input("Ingrese Precio por hora del curso: \t"))
        l_TipoCurso = input("Ingrese el tipo de curso:\t")   
            
        micursor.execute( SENTENCIA_SQL,(l_IDCurso,l_NombreCurso,l_Descripcion,l_PrecioxHora,l_TipoCurso))
        
        #Realizar Commit
        micursor.commit()
        print("\nOk ... Insercion Exitosa: \n")  


        
    except Exception as e:
        print("\n \t Ocurrió un error al consultar a SQL Server: \n\n", e)


# Función eliminar registros
def eliminar_registro(conexion):
    
    try:
    #Crear Cursor
        micursor = conexion.cursor()
        
        SENTENCIA_SQL = """DELETE FROM Cursos
        WHERE IDCurso=?"""
        ## Ingreso de Informacion
        print("\n\t Eliminar Registro de Curso:\n")
        l_IDCurso = int(input("Ingrese ID del Curso a Elimnar: \t"))
        
        micursor.execute( SENTENCIA_SQL,(l_IDCurso))
        micursor.commit()   
        print("Ok ... Eliminacion Exitosa: \n")

        
    except Exception as e:
        print("\n \t Ocurrió un error al consultar a SQL Server: \n\n", e)


# Función actualizar registros
def actualizar_registro(conexion):

    try:

        #Crear Cursor
        micursor = conexion.cursor()
        
        SENTENCIA_SQL = """UPDATE Cursos
        SET PrecioxHora = ?
        WHERE IDCurso= ?"""
        ## Ingreso de Informacion
        print("\n\t Actualizar Precio del Curso:\n")
        l_IDCurso = int(input("Ingrese ID del Curso: \t"))
        l_PrecioxHora = input("Ingrese Nuevo Precio del Curso: \t")
        micursor.execute( SENTENCIA_SQL,(l_PrecioxHora,l_IDCurso))
        
        micursor.commit()
        print("\nOk ... Actualización Exitosa: \n")

        
    except Exception as e:
        print("\n \t Ocurrió un error al consultar a SQL Server: \n\n", e)




# Función mostrar opciones
def mostrar_opciones_crud():
    print("\t****************************")  
    print("\t** SISTEMA CRUD UDEMYTEST **")  
    print("\t****************************")  
    print("\tOpciones CRUD:\n")
    print("\t1. Crear registro")
    print("\t2. Consultar registros")
    print("\t3. Actualizar registro")
    print("\t4. Eliminar registro")
    print("\t5. Salir\n\n")


# Función opciones
def menu(opcion, conexion):
    while True:
        if opcion == '1':
            #crear_registro(conexion)
            insertar_registro(conexion)
        elif opcion == '2':
            #leer_registros(conexion)
            consultar_registro(conexion)
        elif opcion == '3':
            actualizar_registro(conexion)
        elif opcion == '4':
            eliminar_registro(conexion)
        elif opcion == '5':
            print("Saliendo del programa..\n\n.")
            break
        else:
            print("Opción no válida.")   
            break 

        mostrar_opciones_crud()
        opcion = input("Seleccione una opción 1-5:\t")






### Inicio  Programa principal ########
# 1. Importar Biblioteca de conexión
import pyodbc
import json

with open("config.json") as config:
    datos = json.load(config)
    name_server = datos["sql_server"]["name_server"]
    database = datos["sql_server"]["database"]
    username = datos["sql_server"]["user"]
    password = datos["sql_server"]["password"]


controlador_odbc='SQL Server'

# 3. Crear Cadena de Conexion.
connection_string = f'DRIVER={controlador_odbc};SERVER={name_server};DATABASE={database};UID={username};PWD={password}'

#4. Establece la conexión
try:
    conexion = pyodbc.connect(connection_string) 
except Exception as e:
    print("\n \t Ocurrió un error al conectar a SQL Server: \n\n", e)    
# Fin Conexion de BDD
else:  
    mostrar_opciones_crud()
    opcion = input("Seleccione una opción 1-5:\t")
    menu(opcion, conexion)
finally:
    print("Conexion Cerrada: \n")
