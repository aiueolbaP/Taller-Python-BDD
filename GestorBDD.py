import pyodbc
import json


class GestorBDD:
    def __init__(self):
        self.conexion = None
        try:
            with open("config.json") as config:
                data = json.load(config)
                driver = "SQL SERVER"
                user = data["voidsound"]["user"]
                password = data["voidsound"]["password"]
                server = data["voidsound"]["name_server"]
                database = data["voidsound"]["database"]
            
            self.connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}'

            
            self.conexion = pyodbc.connect(self.connection_string)

        except Exception as e:
            print("Hubo un error al conectarse a la base \n", e)



    def consultar(self):
        try:
            print("\n ---------Consultar Canciones--------- \n")

            SQL_QUERY = """
                        SELECT  id_cancion, nombreCancion, duracion, estado, Album_id_album, Genero_id_genero FROM Contenido.Cancion
                        """

            cursor = self.conexion.cursor()
            cursor.execute(SQL_QUERY)
            records = cursor.fetchall()
            print("ID Canción | Nombre | Duracion (seg) | Estado | Id Album | ID Genero")
            for r in records:
                print(f"{r.id_cancion}\t|\t{r.nombreCancion}\t|\t{r.duracion}\t|\t{r.estado}\t|\t{r.Album_id_album}\t|\t{r.Genero_id_genero}")

        except Exception as e:
            print("\n \t Ocurrió un error al consultar a SQL Server: \n\n", e)     


    def insertar(self):
        try:
            print("\n ---------Ingresar Canción--------- \n")

            QUERY_ALBUM = """ select id_album, nombreAlbum from Contenido.Album """

            QUERY_GENEROS = """ select id_genero, nombreGenero from Contenido.Genero """

            SQL_QUERY = """INSERT INTO Contenido.Cancion (id_cancion, nombreCancion, duracion, estado, Album_id_album, Genero_id_genero) 
                        VALUES (?,?,?,?,?,?)"""

            cursor = self.conexion.cursor()

            cursor.execute(QUERY_ALBUM)

            #Se hace un diccionario con cada resultado r[0] es el id vuelto string y r[1] el nombre
            albumes = { str(r[0]): r[1] for r in cursor.fetchall()}

            cursor.execute(QUERY_GENEROS)

            #Lo mismo para generos
            generos = { str(r[0]): r[1] for r in cursor.fetchall()}

            id = int(input("Ingrese id de la canción a seleccionar: "))
            nombre = input("Ingrese el nombre de la canción a ingresar: ")
            duracion = int(input("Ingrese la duración en segundos de la cancion: "))
            estado = input("La canción está: activa o inactiva: ")
            
            print("Albumes disponibles")
            for idAlbum, nombreAlbum in albumes.items():
                print(f'{idAlbum} - {nombreAlbum}')

            album = (input("Ingrese el id del album: "))

            if album not in albumes:
                print("Opción inválida")
                return
            
            print("Géneros disponibles")
            for idGenero, nombreGenero in generos.items():
                print(f'{idGenero} - {nombreGenero}')

            genero = (input("Ingrese el id del género: "))

            if genero not in generos:
                print("Opción inválida")
                return
            
            cursor.execute(SQL_QUERY, (id,nombre,duracion,estado,album,genero))
            cursor.commit()

            print("Inserción realizada con éxito!")
            cursor.close()
        except Exception as e:
            print("Hubo un error durante el proceso \n", e)


    def eliminar(self):

        try:
            SQL_QUERY = """ delete from Contenido.Cancion WHERE id_cancion = ? """

            cursor = self.conexion.cursor()

            print ("----------Eliminar Canción----------")

            cursor.execute("""SELECT id_cancion, nombreCancion FROM Contenido.Cancion""")
            records = cursor.fetchall()

            for r in records:
                print(f'{r.id_cancion} - {r.nombreCancion}')

            id = int(input("Ingrese id de la canción a eliminar: "))

            cursor.execute(SQL_QUERY, (id))
            cursor.commit()
            print("Eliminación exitosa")
        except Exception as e:
            print("Error al eliminar canción\n", e)


    def actualizar(self):
        try:
            
            cursor = self.conexion.cursor()

            print("----------Actualizar canción----------")

            cursor.execute("""SELECT id_cancion, nombreCancion FROM Contenido.Cancion""")
            records = cursor.fetchall()

            for r in records:
                print(f'{r.id_cancion} - {r.nombreCancion}')

            id = int(input("Ingrese id de la canción a actualizar: "))

            cursor.execute("""SELECT  nombreCancion, duracion, estado, Album_id_album, Genero_id_genero 
                           FROM Contenido.Cancion 
                           WHERE id_cancion = ?""", (id, ))
            
            registro = cursor.fetchone()

            if not registro:
                print("No se encontró una canción con ese ID")
                return
            #Si devuelve ('asd', 100, 'activa', '1', '1') se guardan en ese orden en las variables
            nomAc, durAc, estAc, albAc, genAc = registro

            print(f'\nInformación Actual: \nNombre: {nomAc}\nDuración: {durAc}\nEstado: {estAc}\nÁlbum: {albAc}\nGénero: {genAc}')

            cambiar = input("Cambiar nombre actual? (y/n): ").lower()
            nombre = input("Ingrese el nuevo nombre de la canción: ") if cambiar == "y" else nomAc

            cambiar = input("Cambiar duración actual? (y/n): ").lower()
            duracion = int(input("Ingrese la nueva duración en segundos de la canción: ")) if cambiar == "y" else durAc

            cambiar = input("Cambiar estado actual? (y/n): ").lower()
            if cambiar == "y":
                print("1. activa | 2. inactiva")
                est_op = input("Seleccione (1/2): (Cualquier ingreso adicional es considerado inactiva) ")
                estado = "activa" if est_op == '1' else "inactiva"
            else:
                estado = estAc


            cambiar = input("Cambiar album actual? (y/n): ").lower()
            if cambiar == "y":
                cursor.execute(" select id_album, nombreAlbum from Contenido.Album ")
                albumes = { str(r[0]): r[1] for r in cursor.fetchall()}
                print("Albumes disponibles")
                for idAlbum, nombreAlbum in albumes.items():
                    print(f'{idAlbum} - {nombreAlbum}')

                album = (input("Ingrese el id del album: (Cualquier opción inválida terminará el proceso)"))
                if album not in albumes:
                    return
            else:
                album = albAc
            
            cambiar = input("Cambiar el género actual? (y/n): ").lower()
            if cambiar == "y":
                cursor.execute(" select id_genero, nombreGenero from Contenido.Genero ")
                generos = { str(r[0]): r[1] for r in cursor.fetchall()}
                print("Generos disponibles")
                for idGenero, nombreGenero in generos.items():
                    print(f'{idGenero} - {nombreGenero}')

                genero = (input("Ingrese el id del género: (Cualquier opción inválida terminará el proceso)"))
                if genero not in generos:
                    return
            else:
                genero = genAc

            SQL_UPDATE = """
            UPDATE Contenido.Cancion 
            SET nombreCancion = ?, duracion = ?, estado = ?, Album_id_album = ?, Genero_id_genero = ?
            WHERE id_cancion = ?
            """

            cursor.execute(SQL_UPDATE, (nombre, duracion, estado, album, genero, id))
            cursor.commit()
            
            print("Registro actualizado con éxito!")
        except Exception as e:
            print("Hubo un error al actualizar la canción,", e)

            

