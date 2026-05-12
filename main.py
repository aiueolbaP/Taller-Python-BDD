from GestorBDD import GestorBDD

class Menu:
    def __init__(self):
        self.db = GestorBDD()


        if self.db.conexion:
            self.menuprincipal()

    def mostrarMenu(self):
        print("\t****************************")  
        print("\t** SISTEMA CRUD VOIDSOUND **")  
        print("\t****************************")  
        print("\tOpciones CRUD:\n")
        print("\t1. Crear registro")
        print("\t2. Consultar registros")
        print("\t3. Actualizar registro")
        print("\t4. Eliminar registro")
        print("\t5. Salir\n\n")


    def menuprincipal(self):
        
        self.mostrarMenu()
        opcion = input("Ingrese una opcion: ")

        while True:
            if opcion == '1':
                
                self.db.insertar()
            elif opcion == '2':
                
                self.db.consultar()
            elif opcion == '3':
                self.db.actualizar()
            elif opcion == '4':
                
                self.db.eliminar()
            elif opcion == '5':
                print("Saliendo del programa..\n\n.")
                break
            else:
                print("Opción no válida.")   
                break 

            self.mostrarMenu()
            opcion = input("Seleccione una opción 1-5:\t")  

if __name__=="__main__" :
    Menu()
