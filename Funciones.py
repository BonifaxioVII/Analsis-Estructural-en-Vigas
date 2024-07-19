import Metodos as M

def main():  None
if __name__ == "__main__":  main()

class Modelo:
    #Crea todos los componentes de una distribucion
    def __init__(self, longitud_barra) -> None:
        #Unidades
        unidad_carga, unidad_long = "N", "m"
        unidad_cargas_dist=unidad_carga+"/"+unidad_long
        unidad_momentos=unidad_carga+"*"+unidad_long
        self.Unidades = {"UCarga": unidad_carga, "ULong": unidad_long, "UCargaDist": unidad_cargas_dist, "UMomentos": unidad_momentos}

        #Componentes de la distribucion
        self.LenBarra = longitud_barra
        self.Soportes = {1:[],2:[],3:[],"Total":0} #1: Soporte tipo I (Restringe ejes x, y) 2: Soporte tipo II (Restringe eje y), 3: Soporte tipo III (Soporte de pared)
        self.CargasPuntuales = {}
        self.CargasDistribuidas = {}
        self.Momentos = {}

        #Cotas y nombres importantes
        self.Cotas = [0,longitud_barra]

        #Imagen
        self.imagen = M.datar_imagen(self)
        M.mostrar_imagen(self.imagen,"Primer paso") # Muestra la imagen


    #.______________________________________________________________________________________________________________________________________.


    def soportes(self):
        # Protocolo de maximo de soportes
        while True:
            if self.Soportes["Total"] == 2:
                M._except(2, f"""Maximo de soportes: 2 \nSoportes colocados:{self.Soportes["Total"]} (los soportes tipo III valen por 2)""")
                return

            # Panel de opciones
            opcion=str(M._input(f"""Maximo de soportes: 2 \nSoportes colocados:{self.Soportes["Total"]} (los soportes tipo III valen por 2)\n\nElija el tipo de soporte.\n1. Soporte que restringe los ejes 'x' y 'y'.\n2. Soporte que restringe el eje 'y'.\n3. Soporte que restringe el eje 'x' y tiene un momento asociado.\nSALIR.""",int,["Salir"],["1","3"]))
            if opcion == "Salir": return 

            # Agregar primer tipo de soporte
            if opcion == "1":
                while True:
                    posicion = M._input(f"""Posición del soporte ({self.Unidades["ULong"]})""",float,["Salir"],["0",str(self.LenBarra)])
                    if posicion == "Salir": break
                    #Certificar posición
                    if posicion in self.Soportes[1] or posicion in self.Soportes[2]: 
                        M._except(2,"Ya existe este soporte. Intente de nuevo")
                        continue
        
                    # Actualiza soportes
                    self.Soportes["Total"] = self.Soportes["Total"]+1
                    self.Soportes[1].append(posicion)

                    break

            # Agregar segundo tipo de soporte
            elif opcion == "2":
                while True:
                    posicion = M._input(f"""Posición del soporte ({self.Unidades["ULong"]})""",float,["Salir"],["0",str(self.LenBarra)])
                    if posicion == "Salir": break
                    #Certificar posición
                    if posicion in self.Soportes[1] or posicion in self.Soportes[2]: 
                        M._except(2,"Ya existe este soporte. Intente de nuevo")
                        continue

                    # Actualiza soportes
                    self.Soportes["Total"]  = self.Soportes["Total"]+1
                    self.Soportes[2].append(posicion)

                    break
            
            # Agregar tercer tipo de soporte
            else:
                if self.Soportes["Total"] > 0: 
                    M._except(2,"Agregar un soporte de este tipo implicaría reducir los grados de libertad. \nTrate de nuevo")
                    continue
                
                while True:
                    posicion = M._input("En que esquina de la barra estará el soporte. \n1 para la derecha. \n2 para la izquierda.",int,["Salir"],["1","2"])
                    if posicion == "Salir": break 

                    # Actualizar cotas y soportes
                    self.Soportes["Total"]  = self.Soportes["Total"]+2
                    self.Soportes[3].append(0 if posicion == 1 else self.LenBarra)

                    break

            #Actualiza cotas
            self.Cotas = M.actualiza_cotas(self)
            #Mostrar imagen
            self.imagen = M.datar_imagen(self)
            M.mostrar_imagen(self.imagen,"Atlante")


    #.______________________________________________________________________________________________________________________________________.


    def cargas_puntuales(self):
        # Todo cargas_p
        while True:
            M.borrarPantalla()
            # Posicion de la carga
            posicion=M._input(f"""Inserte la ubicacion de la carga puntual ({self.Unidades["ULong"]}).""",float,["Salir"],["0",str(self.LenBarra)])
            if posicion == "Salir":  return

            # Magnitud de la carga
            magnitud=M._input(f"""Posición: {str(posicion)+self.Unidades["ULong"]}\nInserte la magnitud de la carga ({self.Unidades["UCarga"]}).""",float,["Salir"],["0.0001","10000"])
            if magnitud == "Salir": continue

            # Direccion de la carga
            direccion=M._input(f"""Posición: {str(posicion)+self.Unidades["ULong"]}\nMagnitud: {str(magnitud)+self.Unidades["UCarga"]}\nInserte la dirección de la carga puntual \n1. '↑' \n2. '↓' """,int,["Salir"],["1","2"])
            if direccion == "Salir": continue

            M.borrarPantalla()
            print(f"""Posición: {str(posicion)+self.Unidades["ULong"]}\nMagnitud: {str(magnitud)+self.Unidades["UCarga"]}\nDirección: {"↑" if direccion==1 else "↓"}""")
            
            # Actualizar cotas y modelo
            self.CargasPuntuales[len(self.CargasPuntuales)+1]  = {"Direccion":direccion,"Magnitud":magnitud,"Posicion":posicion}            
            self.Cotas = M.actualiza_cotas(self)
            
            #Mostrar imagen
            self.imagen = M.datar_imagen(self)
            M.mostrar_imagen(self.imagen,"SkyCiv me la pela")


    #.______________________________________________________________________________________________________________________________________.


    def cargas_distribuidas(self):
        while True:
            #Posiciones iniciales y finales de la carga
            posicion_inicial = M._input(f"""Posición inicial de la carga distribuida ({self.Unidades["ULong"]}). """,float,["Salir"],["0",str(self.LenBarra)])
            if posicion_inicial=="Salir": return

            posicion_final=M._input(f"""Posición inicial: {str(posicion_inicial)+self.Unidades["ULong"]}\nPosición final de la carga distribuida ({self.Unidades["ULong"]}). """,float,["Salir"],[str(posicion_inicial),str(self.LenBarra)])
            if posicion_final=="Salir": continue
            
            #Cargas finales e iniciales
            carga_inicial=M._input(f"""Posición inicial: {str(posicion_inicial)+self.Unidades["ULong"]}\nPosición final: {str(posicion_final)+self.Unidades["ULong"]} \n\nCarga inicial de la carga distribuida ({self.Unidades["UCargaDist"]}).""",float,["Salir"],["0","10000"]) 
            if carga_inicial=="Salir": continue

            carga_final=M._input(f"""Posición inicial: {str(posicion_inicial)+self.Unidades["ULong"]}\nPosición final: {str(posicion_final)+self.Unidades["ULong"]}\n\nCarga inicial: {str(carga_inicial)+self.Unidades["UCargaDist"]}\nCarga final de la carga distribuida ({self.Unidades["UCargaDist"]}).""",float,["Salir"],["0","10000"])
            if carga_final=="Salir": continue
                        
            #Direccion
            direccion=M._input(f"""Posición inicial: {str(posicion_inicial)+self.Unidades["ULong"]}\nPosición final: {str(posicion_final)+self.Unidades["ULong"]}\n\nCarga inicial: {str(carga_inicial)+self.Unidades["UCargaDist"]}\nCarga final: {str(carga_final)+self.Unidades["UCargaDist"]}\n\nInserte la dirección de la carga distribuida \n1. '↑' \n2. '↓' """,int,["Salir"],["1","2"])
            if direccion == "Salir":continue

            M.borrarPantalla()
            print(f"""Posición inicial: {str(posicion_inicial)+self.Unidades["ULong"]}\nPosición final: {str(posicion_final)+self.Unidades["ULong"]}\n\nCarga inicial: {str(carga_inicial)+self.Unidades["UCargaDist"]}\nCarga final: {str(carga_final)+self.Unidades["UCargaDist"]}\n\nDireccion: {"↑" if direccion==1 else "↓"}""")
            
            # Actualizar cotas y modelo
            self.CargasDistribuidas[len(self.CargasDistribuidas)+1] = {"Posiciones":(posicion_inicial,posicion_final),"Magnitudes":(carga_inicial,carga_final),"Direccion":direccion}
            self.Cotas = M.actualiza_cotas(self)

            #Mostrar imagen
            self.imagen = M.datar_imagen(self)
            M.mostrar_imagen(self.imagen,"Chegg me la pela")


    #.______________________________________________________________________________________________________________________________________.


    def momentos(self):
        while True:
            #Posicion del momento
            posicion=M._input(f"""Posicion del momento ({self.Unidades["ULong"]}):""",float,["Salir"],["0",str(self.LenBarra)])
            if posicion == "Salir": return

            #Magnitud del momento
            magnitud=M._input(f"""Posicion: {str(posicion)+self.Unidades["ULong"]}\nValor del momento ({self.Unidades["UMomentos"]}): """,float,["Salir"],["0.00001","10000000"])
            if magnitud == "Salir": continue

            #Direccion del momento
            direccion=M._input(f"""Posicion: {str(posicion)+self.Unidades["ULong"]}\nMagnitud: {str(magnitud)+self.Unidades["UMomentos"]}\nDirección del momento: \n1. + ↶ \n2. - ↷ """,int,["Salir"],["1","2"])
            if direccion == "Salir": continue

            M.borrarPantalla()
            print(f"""Posicion: {str(posicion)+self.Unidades["ULong"]}\nMagnitud: {str(magnitud)+self.Unidades["UMomentos"]}\nDirección: {"↶" if direccion == 1 else "↷"}""")

            # Actualizar cotas y modelo
            self.Momentos[len(self.Momentos)+1] = {"Posicion":posicion, "Magnitud":magnitud, "Direccion":direccion}          
            self.Cotas = M.actualiza_cotas(self)

            #Mostrar imagen
            self.imagen = M.datar_imagen(self)
            M.mostrar_imagen(self.imagen,"Tú me la pelas")  


    #.______________________________________________________________________________________________________________________________________.


    def ajustes(self):
        while True:
            M.borrarPantalla()
            #interfaz
            opcion = str(M._input(f"""Configuración general del modelo: \n\nUnidades: \nUnidad de carga: {self.Unidades["UCarga"]} \nUnidad de longitud: {self.Unidades["ULong"]} \n\nTamaño de imagen: \nLargo en x: {str(M.largo_x)+" pixeles"} \nLargo en y: {str(M.largo_y)+" pixeles"}\n\n\nConfiguracion especifica del modelo: \nLongitud de barra: {self.LenBarra} \nSoportes: {self.Soportes} \nCargas puntuales: {self.CargasPuntuales} \nCargas distribuidas: {self.CargasDistribuidas} \nMomentos: {self.Momentos}\n\n¿Que desea ver/reconfigurar? (Para más opciones sugierale al proveedor más cercano)\n1. Unidades \n2. Tamaño de imagen \n3. Modelo \n4. Salir""",int,["Salir"],["1","4"]))
            if opcion == "Salir" or opcion == "4": return

            #cambiar unidades
            if opcion == "1":
                while True:
                    #Interfaz 2
                    opcion_2 = str(M._input(f"""Ver/Reconfigurar Unidades \nUnidad de carga: {self.Unidades["UCarga"]} \nUnidad de longitud: {self.Unidades["ULong"]} \nUnidad de carga distribuida: {self.Unidades["UCargaDist"]} \nUnidad de momentos: {self.Unidades["UMomentos"]} \n\nOpciones: \n1. Cambiar unidad de carga \n2. Cambiar unidad de longitud \n3. Salir""", int, ["Salir"], ["1", "3"]))
                    if opcion_2 == "Salir" or opcion_2 == "3": break

                    #Unidad de carga
                    if opcion_2 == "1":
                        new_unidad_carga = str(M._input("Ver/Reconfigurar Unidades \nInserte la nueva unidad de carga",str,["Salir","SALIR"],formato_titulo=False))
                        if new_unidad_carga == "Salir": continue

                        self.Unidades["UCarga"] = new_unidad_carga
                    
                    #Unidad de longitud
                    else:
                        new_unidad_long = str(M._input("Ver/Reconfigurar Unidades \nInserte la nueva unidad de longitud",str,["Salir","SALIR"],formato_titulo=False))
                        if new_unidad_long == "Salir": continue

                        self.Unidades["ULong"] = new_unidad_long

                    self.Unidades["UCargaDist"] = self.Unidades["UCarga"]+"/"+self.Unidades["ULong"]
                    self.Unidades["UMomentos"] = self.Unidades["UCarga"]+"*"+self.Unidades["ULong"]

            #cambiar tamaño de la imagen
            if opcion == "2":
                while True:
                    #Interfaz 2
                    opcion_3 = str(M._input(f"""Ver/Reconfigurar Tamaño de la imagen \nAncho: {str(M.largo_y)+" pixeles"} \nLargo: {str(M.largo_x)+" pixeles"}\n\nOpciones: \n1. Cambiar ancho \n2. Cambiar largo \n3. Salir""", int, ["Salir"], ["1", "3"]))
                    if opcion_3 == "Salir" or opcion_3 == "3": break

                    #cambiar ancho/largo_y
                    if opcion_3 == "1":
                        new_ancho = str(M._input("Ver/Reconfigurar Tamaño de la imagen \nInserte el nuevo ancho (en pixeles) - max: 650",int,["Salir"],["0","650"]))
                        if new_ancho == "Salir": continue

                        M.largo_y = int(new_ancho)
                    
                    #Unidad largo/largo_x
                    else:
                        new_largo = str(M._input("Ver/Reconfigurar Tamaño de la imagen \nInserte el nuevo largo (en pixeles) - max: 1300",int,["Salir"],["0","1300"]))
                        if new_largo == "Salir": continue

                        M.largo_x = int(new_largo)
                    
                    M.max_x, M.min_x = int(M.largo_x-(M.largo_x/10)), int(M.largo_x/10)
                    M.max_y, M.min_y = int(M.largo_y-(M.largo_y/10)), int(M.largo_y/10)

            #modelo
            if opcion == "3":
                while True:
                    M.mostrar_imagen(self.imagen,"¿Te gusta lo que ves?")
                    
                    #Interfaz 3
                    opcion_4 = str(M._input(f"""Ver/Reconfigurar Modelo \nLongitud de barra: {self.LenBarra} \nSoportes: {self.Soportes} \nCargas puntuales: {self.CargasPuntuales} \nCargas distribuidas: {self.CargasDistribuidas} \nMomentos: {self.Momentos} \nCotas: {self.Cotas}\n\nOpciones: \n1. Borrar todo \n2. Borrar un soporte \n3. Borrar una carga puntual \n4. Borrar una carga distribuida \n5. Borrar un momento \n6. Salir""", int, ["Salir"], ["1", "6"]))
                    if opcion_4 == "Salir" or opcion_4 == "6": break

                    #Borrar todo
                    if opcion_4 == "1":
                        del self
                        M._except(3,"Eliminando...")
                        return False

                    #Borrar soportes
                    if opcion_4 == "2":
                        while True:
                            if self.Soportes["Total"] == 0: #Si no hay soportes
                                M._except(3,"No hay soportes colocados en el modelo")
                                break
                        
                            #Enumeracion de los soportes
                            num_soporte = 0
                            texto = ""
                            dict_referencia = {} #Diccionario que se llena con las opciones que existen para borrar
                            for key, value in self.Soportes.items():
                                if type(key) == str or len(value) == 0: continue
                                for posicion in value:
                                    num_soporte += 1
                                    texto = texto + f"""{num_soporte}. Soporte tipo {key}, posicion {str(posicion)+self.Unidades["ULong"]} \n"""
                                    dict_referencia[num_soporte] = {"Tipo": key, "Posicion": posicion}

                            #Interfaz parcial
                            opcion_4_1 = str(M._input(f"""Ver/Reconfigurar Modelo - Borrar Soporte \n\nSeleccione el soporte que borrará: \n{texto}""", int, ["Salir"], ["1", str(num_soporte)]))
                            if opcion_4_1 == "Salir": break

                            self.Soportes[dict_referencia[int(opcion_4_1)]["Tipo"]].remove(dict_referencia[int(opcion_4_1)]["Posicion"])
                            self.Soportes["Total"] -= 1 if dict_referencia[int(opcion_4_1)]["Tipo"] != 3 else 2

                    #Borrar carga puntual
                    if opcion_4 == "3":
                        while True:
                            if len(self.CargasPuntuales) == 0: #Si no hay cargas puntuales
                                M._except(3,"No hay cargas puntuales colocadas en el modelo")
                                break
                        
                            #Enumeracion de las cargas puntuales
                            texto = ""
                            for key, value in self.CargasPuntuales.items():
                                texto = texto + f"""{key}. Magnitud {str(value["Magnitud"])+self.Unidades["UCarga"]}, Posicion {str(value["Posicion"])+self.Unidades["ULong"]}, Dirección {"↑" if value["Direccion"]==1 else "↓"} \n"""

                            #Interfaz parcial
                            opcion_4_2 = str(M._input(f"""Ver/Reconfigurar Modelo - Borrar carga puntual \n\nSeleccione la carga puntual que borrará: \n{texto}""", int, ["Salir"], ["1", str(len(self.CargasPuntuales))]))
                            if opcion_4_2 == "Salir": break

                            del self.CargasPuntuales[int(opcion_4_2)]

                            #Actualizar diccionario cargas puntuales
                            for carga_antigua in range(int(opcion_4_2) + 1, len(self.CargasPuntuales) + 2):
                                self.CargasPuntuales[carga_antigua-1] = self.CargasPuntuales.pop(carga_antigua)
                    
                    #Borrar carga distribuida
                    if opcion_4 == "4":
                        while True:
                            if len(self.CargasDistribuidas) == 0: #Si no hay cargas distribuidas
                                M._except(3,"No hay cargas distribuidas colocadas en el modelo")
                                break
                        
                            #Enumeracion de las cargas distribuidas
                            texto = ""
                            for key, value in self.CargasDistribuidas.items():
                                texto = texto + f"""{key}. Magnitudes {str(value["Magnitudes"])+self.Unidades["UCargaDist"]}, Posiciones {str(value["Posiciones"])+self.Unidades["ULong"]}, Dirección {"↑" if value["Direccion"]==1 else "↓"} \n"""

                            #Interfaz parcial
                            opcion_4_3 = str(M._input(f"""Ver/Reconfigurar Modelo - Borrar carga distribuida \n\nSeleccione la carga distribuida que borrará: \n{texto}""", int, ["Salir"], ["1", str(len(self.CargasDistribuidas))]))
                            if opcion_4_3 == "Salir": break

                            del self.CargasDistribuidas[int(opcion_4_3)]
                            
                            #Actualizar diccionario cargas distribuidas
                            for carga_antigua in range(int(opcion_4_3) + 1, len(self.CargasDistribuidas) + 2):
                                self.CargasDistribuidas[carga_antigua-1] = self.CargasDistribuidas.pop(carga_antigua)

                    #Borrar momentos
                    if opcion_4 == "5":
                        while True:
                            if len(self.Momentos) == 0: #Si no hay momentos
                                M._except(3,"No hay momentos en el modelo")
                                break
                        
                            #Enumeracion de los momentos
                            texto = ""
                            for key, value in self.Momentos.items():
                                texto = texto + f"""{key}. Magnitud {str(value["Magnitud"])+self.Unidades["UMomentos"]}, Posicion {str(value["Posicion"])+self.Unidades["ULong"]}, Dirección {"↶" if value["Direccion"] == 1 else "↷"} \n"""

                            #Interfaz parcial
                            opcion_4_4 = str(M._input(f"""Ver/Reconfigurar Modelo - Borrar momento \n\nSeleccion el momento que borrará: \n{texto}""", int, ["Salir"], ["1", str(len(self.Momentos))]))
                            if opcion_4_4 == "Salir": break

                            del self.Momentos[int(opcion_4_4)]

                            #Actualizar diccionario momentos
                            for momento_antiguo in range(int(opcion_4_4) + 1, len(self.Momentos) + 2):
                                self.Momentos[momento_antiguo-1] = self.Momentos.pop(momento_antiguo)

                    #Actualizar cotas
                    self.Cotas = M.actualiza_cotas(self)

                    #Actualizar imagen
                    self.imagen = M.datar_imagen(self)

            self.imagen = M.datar_imagen(self)


    #.______________________________________________________________________________________________________________________________________.


    def resolver(self):
        #Valores de cada soporte con procedimiento
        valores_soportes = M.valor_soportes(self)
        if valores_soportes is None: return

        #Transforma los valores de los soportes como cargas puntuales y momentos si es el caso
        self.CargasPuntualesGenerales = self.CargasPuntuales.copy() #Cargas puntuales con los valores de los soportes
        self.MomentosGenerales = self.Momentos.copy() #Momentos con los valores de los soportes
        
        if len(self.Soportes[3]) != 0: #En caso de existir un soporte tipo 3
            magnitud_asociado = valores_soportes["S_y"]
            momento_asociado = valores_soportes["SM"]
            self.CargasPuntualesGenerales[len(self.CargasPuntualesGenerales)+1] = {"Direccion": 1 if magnitud_asociado > 0 else 2, "Magnitud": abs(magnitud_asociado), "Posicion": self.Soportes[3][0]}   
            self.MomentosGenerales[len(self.Momentos)+1] = {"Posicion":self.Soportes[3][0], "Magnitud": abs(momento_asociado), "Direccion": 1 if momento_asociado > 0 else 2}    
            del magnitud_asociado, momento_asociado
        else: #Para soportes tipo 1 y 2
            for key, value in valores_soportes.items():
                self.CargasPuntualesGenerales[len(self.CargasPuntualesGenerales)+1] = {"Direccion": 1 if value > 0 else 2, "Magnitud": abs(value), "Posicion": key}   

    
        #**************************************Funcion de cargas*************************************
        def FuerzaCortante():
            M.borrarPantalla()
            print("Cargando...")
            
            #Funcion carga
            f_carga = M.funcion_carga(self)
            f_carga_array = f_carga.f_array()

            #interfaz
            funcion_sympy = f_carga.f_sympy()
            #Funcion de carga a trozos
            interfaz = f"""Diagrama de cargas: \nDonde 'f' se refiere a la fuerza ({self.Unidades["UCarga"]}) en un posición de la barra 'x' ({self.Unidades["ULong"]}) dada.     0 <= x <= {self.LenBarra} \n"""
            interfaz = interfaz + "\nf(x) ="
            for funcion in funcion_sympy: interfaz = interfaz + f"""\n| {funcion["rang_ini"]} <= x < {funcion["rang_fin"]} : {funcion["funcion"]}"""
            #Magnitud maximo y minimo de la funcion de carga
            extremos = f_carga.extremos()
            MaxCarga, MinCarga = extremos["Max"], extremos["Min"]
            
            interfaz = interfaz + f"""\n\nMax: f({MaxCarga["posicion"]}) = {MaxCarga["magnitud"]}{self.Unidades["UCarga"]}"""
            interfaz = interfaz + f"""\nMin: f({MinCarga["posicion"]}) = {MinCarga["magnitud"]}{self.Unidades["UCarga"]}"""

            #Graficacion de la funcion array
            print(interfaz)
            M.graficas_cargas(self, f_carga_array)

            #Interfaz de opciones para el diagrama de cargas
            while True:
                Posiciones = M._input(interfaz + f"""\n\nPara consultar la carga de una posición dada en la barra, inserte la posición ({self.Unidades["ULong"]}). \nSi quiere ver la imagen sin cotas de carga escriba 'VER' \nSi quiere pasar al diagrama de momentos presione ENTER""", str, ["", "Salir", "Continue", "Ver"])
                if Posiciones == "Salir": return
                elif Posiciones == "Continue" or Posiciones == "": break
                
                #Mostrar cotas carga elegidas por el usuario
                Posiciones = Posiciones.split(",") if Posiciones != "Ver" else []
                Posiciones_int = []
                try: 
                    for x in Posiciones: Posiciones_int.append(float(x)) if 0 <= float(x) and float(x) <= self.LenBarra else M._except(3, "Una posición agregada está fuera del rango establecido") 
                    M.graficas_cargas(self, f_carga_array, Posiciones_int)
                except: M._except(3)
            
        #**************************************Funcion de momentos*************************************
        def MomentoFlector():
            M.borrarPantalla()
            print("Cargando...")

            #Funcion momentos
            f_momentos = M.funcion_momentos(self)
            f_momentos_array = f_momentos.f_array()
            
            #interfaz
            funcion_sympy = f_momentos.f_sympy()
            #Funcion de momentos a trozos
            interfaz = f"""Diagrama de momentos: \nDonde 'M' se refiere a la magnitud de momento ({self.Unidades["UMomentos"]}) en un posición de la barra 'x' ({self.Unidades["ULong"]}) dada.     0 <= x <= {self.LenBarra} \n"""
            interfaz = interfaz + "\nM(x) ="
            for funcion in funcion_sympy: interfaz = interfaz + f"""\n| {funcion["rang_ini"]} <= x < {funcion["rang_fin"]} : {funcion["funcion"]}"""
            #Magnitud maximo y minimo de la funcion de momentos
            extremos = f_momentos.extremos()
            MaxMomentos, MinMomentos = extremos["Max"], extremos["Min"]
            
            interfaz = interfaz + f"""\n\nMax: f({MaxMomentos["posicion"]}) = {MaxMomentos["magnitud"]}{self.Unidades["UMomentos"]}"""
            interfaz = interfaz + f"""\nMin: f({MinMomentos["posicion"]}) = {MinMomentos["magnitud"]}{self.Unidades["UMomentos"]}"""
            
            #Graficacion de la funcion array
            print(interfaz)
            M.graficas_momentos(self, f_momentos_array)

            #Interfaz de opciones para el diagrama de momentos
            while True:
                Posiciones = M._input(interfaz + f"""\n\nPara consultar el momento de una posición dada en la barra, inserte la posición ({self.Unidades["ULong"]}). \nSi quiere ver la imagen sin cotas de carga escriba 'VER' \nSi quiere pasar al diagrama de momentos presione ENTER""", str, ["", "Salir", "Continue", "Ver"])
                if Posiciones == "Salir": return
                elif Posiciones == "Continue" or Posiciones == "": break
                
                #Mostrar cotas momentos elegidas por el usuario
                Posiciones = Posiciones.split(",") if Posiciones != "Ver" else []
                Posiciones_int = []

                try:
                    for x in Posiciones: Posiciones_int.append(float(x)) if 0 <= float(x) and float(x) <= self.LenBarra else M._except(3, "Una posición agregada está fuera del rango establecido") 
                    M.graficas_momentos(self, f_momentos_array, Posiciones_int)
                except: M._except(3)
        
        FuerzaCortante()
        MomentoFlector()

        #Eliminar CargasPuntualesGenerales y MomentosGenerales
        del self.CargasPuntualesGenerales, self.MomentosGenerales

        

    #.______________________________________________________________________________________________________________________________________.





    
 
