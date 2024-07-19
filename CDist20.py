import Metodos as M
import Funciones as F

salir = False
while salir == False:
    #Crear la barra
    longitud_barra=M._input("Longitud de la barra ",float,["Salir"],condicion_num=["0.001","1000"])
    if longitud_barra == "Salir": break

    #Crear clase con los datos de la distribucion
    modelo = F.Modelo(longitud_barra)


    #**********************************Panel de opciones*****************************************
    while True:
        if salir == True: break
        M.borrarPantalla()

        #Interfaz
        opcion = str(M._input("¿Que desea agregar?. \n1. Soportes. \n2. Cargas puntuales. \n3. Cargas distribuidas. \n4. Momentos. \n5. Resolver. \n6. Modelo/Ajustes. \n7. Salir.""",int,["Salir"],["1","7"]))
        M.borrarPantalla()

        #Soportes
        if opcion == "1": modelo.soportes()

        #Cargas puntuales
        elif opcion == "2": modelo.cargas_puntuales()

        #Cargas distribuidas
        elif opcion == "3": modelo.cargas_distribuidas()

        #Momentos
        elif opcion == "4": modelo.momentos()

        #Resolver
        elif opcion == "5": modelo.resolver() 
        
        #Modelo/Ajustes
        elif opcion == "6":
            resolucion = modelo.ajustes() #Si la resolucion es falsa, se entenderá como que se eliminó todo, de lo contrario resolucion es None
            if resolucion == False: break

        # Salir
        elif opcion == "7" or opcion == "Salir": salir = True
            