from time import sleep
from sys import exc_info
from os import system, name
import cv2
import numpy as np
from sympy import *
from sympy.calculus.util import *

def main():  None
if __name__ == "__main__":  main()

x = symbols('x')

#Dimensiones de imagen
largo_x = 1000
largo_y = 600

#Dimensiones del contenido
max_x, min_x = int(largo_x-(largo_x/10)), int(largo_x/10)
max_y, min_y = int(largo_y-(largo_y/10)), int(largo_y/10)

#*************************************Generales Importadas***************************************
#Funciones hechas con anterioridad copiadas y pegadas de otros proyectos propios

#Funcion matematica
class Funcion:
    def __init__(self, funcion, variable="x") -> None:
        """Función, recibe expresion sympy|str"""
        if type(funcion) == str: self.funcion = sympify(funcion)
        else: self.funcion = funcion

        if type(variable) == str: self.variable = sympify(variable)
        else: self.variable = variable

    def __f__(self, x):
        """Devuelve el valor de la funcion en un valor x"""
        f = lambdify([self.variable], self.funcion)
        return f(x)

    def inyectiva(self, y, intervalo:tuple = None):
        """Devuelve el valor x dado un termino f(x)
        Si se da un intervalo se devolverá el valor x que pretenezca a su conjunto"""
        #En caso de que la funcion sea una constante, la funcion se cumple en todo el intervalo
        try: 
            float(self.funcion)
            return [f"""{intervalo[0]} <= x <= {intervalo[1]}"""]
        except: pass

        ecuacion = Eq(self.funcion, y)
        solucion = solve(ecuacion) 

        #Comprobar que las soluciones sean reales
        if intervalo is not None:
            solucion_reales = []
            for sol in solucion:
                if sol.is_real != True: sol = sympify(str(sol).replace("I","0"))
                sol = simplify(sol)
                if sol >= intervalo[0] and sol <= intervalo[1]: solucion_reales.append(round(float(sol),5))

        return solucion_reales

    def Max(self, intervalo:tuple = None, posicion = False):
        """Devuelve el maximo local de la función en un intervalo dado. Sin intervalo se devuelve el maximo global de la función
        Con posicion, la funcion devuelve tambien el valor x correspondiente al maximo"""
        if intervalo is not None:
            ivl = Interval(intervalo[0], intervalo[1])
            __max__ =  maximum(self.funcion, self.variable, ivl)
        else: __max__ = maximum(self.funcion, self.variable)
        
        if posicion: return(__max__, self.inyectiva(__max__, intervalo))
        else: return __max__

    def Min(self, intervalo:tuple = None, posicion = False):
        """Devuelve el minimo local de la función en un intervalo dado. Sin intervalo se devuelve el minimo global de la función
        Con posicion, la funcion devuelve tambien el valor x correspondiente al minimo"""
        if intervalo is not None:
            ivl = Interval(intervalo[0], intervalo[1])
            __min__ =  minimum(self.funcion, self.variable, ivl)
        else: __min__ = minimum(self.funcion, self.variable)
        
        if posicion: return(__min__, self.inyectiva(__min__, intervalo))
        else: return __min__

# Cuenta regresiva hacia atras con la pantalla del except
def _except(s,error:str = "."):
    for i in range(s+1):
        borrarPantalla()
        print("Hay un error \n"+str(exc_info()[0])) if error == "." else print(error)
        print("\n\n")
        print(s-i)
        sleep(1)

# Función para borrar pantalla sin importar el software
def borrarPantalla() -> None:
    if name == "posix": system ("clear")
    elif name == "ce" or name == "nt" or name == "dos": system ("cls")

#Función para convertir el texto en formato titulo y borrar espacios iniciales y finales
def form_titleCarr(text:str) -> str:
    text = text.lstrip()
    text = text.rstrip()
    text = text.title()
    return text

#Funcion que restirnge los posibles respuestas a un input
def _input(frase:str, tipo:type, excepcion:list = None, condicion_num:list = None, formato_titulo = True):
    """tipo: Tipo de la respuesta esperada 
    excepcion: lista con los "str" que funcionan como unico valor excepto permitido (Usualmente es Salir)
    condicion_num: lista con los valores numericos permitidos
    formato_titulo: True o False"""
    
    while True:
        if condicion_num is None and excepcion is None:
            try:
                borrarPantalla()
                resultado=tipo(input(frase+"\n>>> "))
            except: 
                _except(2)
                borrarPantalla()
            else: break

        elif condicion_num is None and excepcion is not None:
            try:
                borrarPantalla()
                resultado=form_titleCarr(input(frase+"\n>>> ")) if formato_titulo else input(frase+"\n>>> ")
                if form_titleCarr(resultado) in excepcion: return resultado
                else: resultado=tipo(resultado)
            except: 
                _except(2)
                borrarPantalla()
            else: break

        elif condicion_num is not None and excepcion is None:
            try:
                while True:
                    borrarPantalla()
                    resultado=tipo(input(frase+"\n>>> ")) 
                    if resultado >= float(condicion_num[0]) and resultado <= float(condicion_num[1]):
                        return resultado
                    else: _except(2,"Su numero indicado excede los limites") 
            except: 
                _except(2)
                borrarPantalla()
            else: break
        
        elif condicion_num is not None and excepcion is not None:
            try:
                while True:
                    borrarPantalla()
                    resultado=form_titleCarr(input(frase+"\n>>> ")) if formato_titulo else input(frase+"\n>>> ")
                    if form_titleCarr(resultado) in excepcion: return resultado
                    else:
                        resultado=tipo(resultado)
                        if float(resultado) >= float(condicion_num[0]) and float(resultado) <= float(condicion_num[1]):
                            return resultado
                        else: _except(2,"Su numero indicado excede los limites")       
            except: 
                _except(2)
                borrarPantalla()
            else: break
    
    return resultado


#*******************************Funciones recurrentes en el proyecto********************************************

#Pasa una funcion sympy a un arreglo entre un rango
def funcion_array(rango_t,iteraciones,funcion):
    x = symbols('x', positive=True)
    f = lambdify([x], funcion)

    x = np.linspace(rango_t[0], rango_t[1], iteraciones)
    
    #Creacion del array acotado
    array_final = []
    for i in x: array_final.append(f(i))

    return np.array(array_final)

#Funcion que describe la fuerza puntual de una carga distribuida
def cd_area(carga_inicial,carga_final,posicion_inicial,posicion_final):
    b=carga_inicial
    B=carga_final
    h=(posicion_final-posicion_inicial)

    P=((b+B)/2)*h
    return P

#Funcion que describe el centroide de una carga distribuida
def cd_centroide(carga_inicial,carga_final,posicion_inicial,posicion_final):
    b=carga_inicial
    B=carga_final
    h=(posicion_final-posicion_inicial)
    p_1=posicion_inicial
    if b==0 and B==0: C=p_1
    else: C=p_1+((h-(h*(1/3))*(((2*b)+B)/(b+B))))
    return C
  

#*******************************************Imagenes**************************************************

font = cv2.FONT_HERSHEY_SIMPLEX
#Sirve para crear nuevas imagenes que se adecuaran a los datos del modelo
def datar_imagen(self): 
    #Imagen y dibujo de la barra
    imagen = crear_imagen()    

    #********************************************Extras útiles*************************************************
    Vm = 0 #Valor maximo de magnitud
    #Encontrar la mayor magnitud colocada en cargas puntuales
    for carga in self.CargasPuntuales:
        if self.CargasPuntuales[carga]["Magnitud"] > Vm: Vm = self.CargasPuntuales[carga]["Magnitud"]
    #Encontrar la mayor magnitud colocada en cargas distribuidas
    for carga in self.CargasDistribuidas:
        if self.CargasDistribuidas[carga]["Magnitudes"][0] > Vm: Vm = self.CargasDistribuidas[carga]["Magnitudes"][0]
        if self.CargasDistribuidas[carga]["Magnitudes"][1] > Vm: Vm = self.CargasDistribuidas[carga]["Magnitudes"][1]


    #************************************Agregar elementos a la imagen***********************************************************
    def dibujar_soportes(Soportes):
        FT = int(largo_y/100 + largo_x/100) #Factor tamaño del soporte
        for I in Soportes[1]: #Dibujar soportes tipo I
            #Esquinas
            pt1 = (regla_de_3(self.LenBarra,I)-FT,int(largo_y/2)+ 2*FT)
            pt2 = (regla_de_3(self.LenBarra,I),int(largo_y/2))
            pt3 = (regla_de_3(self.LenBarra,I)+FT,int(largo_y/2)+ 2*FT)
            #Contorno
            cv2.circle(imagen, pt1, 2, (0,255,0), -1)
            cv2.circle(imagen, pt2, 2, (0,255,0), -1)
            cv2.circle(imagen, pt3, 2, (0,255,0), -1)
            triangle_cnt = np.array( [pt1, pt2, pt3] )
            #Terminado
            cv2.drawContours(imagen, [triangle_cnt], 0, (0,255,0), -1)

        for II in Soportes[2]: #Dibujar soportes tipo II
            cv2.circle(imagen,(regla_de_3(self.LenBarra,II),int(largo_y/2)+FT),FT,(0,255,0),-1)
        
        for III in Soportes[3]: #Dibujar soportes tipo II
            pos = min_x if III == 0 else max_x
            cv2.line(imagen,(pos,min_y),(pos,max_y),(0,255,0),3)

    def dibujar_cargas_puntuales(CargasPuntuales):        
        for carga in range(1,len(CargasPuntuales)+1):
            posicion = CargasPuntuales[carga]["Posicion"]
            magnitud = CargasPuntuales[carga]["Magnitud"]
            
            # Imagen
            if CargasPuntuales[carga]["Direccion"] != 1: magnitud = -magnitud
            
            cv2.arrowedLine(imagen, (regla_de_3(self.LenBarra,posicion), conversion(magnitud,Vm)), (regla_de_3(self.LenBarra,posicion),int(largo_y/2)), (0,0,255), 2, tipLength = 0.075)                    
            cv2.putText(imagen,str(CargasPuntuales[carga]["Magnitud"])+self.Unidades["UCarga"],(regla_de_3(self.LenBarra,posicion)+3,conversion(magnitud,Vm)),font,0.5,(0,0,0),1,cv2.LINE_AA)
    
    def dibujar_cargas_distribuidas(CargasDistribuidas):
        for carga in range(1,len(CargasDistribuidas)+1):
            Posiciones = CargasDistribuidas[carga]["Posiciones"]
            Magnitudes = np.array(CargasDistribuidas[carga]["Magnitudes"])

            if CargasDistribuidas[carga]["Direccion"] != 1: Magnitudes = -Magnitudes

            lineas_intermedias = int((regla_de_3(self.LenBarra,Posiciones[1]) - regla_de_3(self.LenBarra,Posiciones[0]))/75) #Cantidad de lines intermedias
            cargas_rango_x = np.linspace(Posiciones[0],Posiciones[1],num=lineas_intermedias+2) #Array con los valores de las posciones que se dibujaran
            cargas_rango_y = np.linspace(Magnitudes[0],Magnitudes[1],num=lineas_intermedias+2) #Array con los valores de las magnitudes que se dibujaran

            # Imagen
            for i in range(lineas_intermedias+2): #Crear carga por carga su respectiva flecha
                posicion = cargas_rango_x[i]
                magnitud = cargas_rango_y[i]
                
                cv2.arrowedLine(imagen, (regla_de_3(self.LenBarra,posicion),conversion(magnitud,Vm)), (regla_de_3(self.LenBarra,posicion),int(largo_y/2)), (0,0,255), 1, tipLength = 0.075)
            
            cv2.line(imagen,(regla_de_3(self.LenBarra,Posiciones[0]),conversion(Magnitudes[0],Vm)),(regla_de_3(self.LenBarra,Posiciones[1]),conversion(Magnitudes[1],Vm)),(0,0,255), 2)
            if Magnitudes[0] != 0: cv2.putText(imagen,str(abs(Magnitudes[0]))+self.Unidades["UCargaDist"],(regla_de_3(self.LenBarra,Posiciones[0])+3,conversion(Magnitudes[0],Vm)),font,0.5,(0,0,0),1,cv2.LINE_AA)
            if Magnitudes[1] != 0: cv2.putText(imagen,str(abs(Magnitudes[1]))+self.Unidades["UCargaDist"],(regla_de_3(self.LenBarra,Posiciones[1])+3,conversion(Magnitudes[1],Vm)),font,0.5,(0,0,0),1,cv2.LINE_AA)

    def dibujar_momentos(Momentos):
        for momento in range(1,len(Momentos)+1):
            posicion = Momentos[momento]["Posicion"]

            # Imagen            
            center_coordinates = (regla_de_3(self.LenBarra,posicion),int(largo_y/2))
            axesLength = (25, 25)
            angle = 0
            color = (0, 0, 0)
            thickness = 2
            if Momentos[momento]["Direccion"] != 1: #↶ 
                startAngle = 0
                endAngle = 270

                cv2.arrowedLine(imagen, (regla_de_3(self.LenBarra,posicion)-1, int(largo_y/2) -25), (regla_de_3(self.LenBarra,posicion), int(largo_y/2) -25), (0,0,0), 2, tipLength = 10)                    
                cv2.putText(imagen,str(Momentos[momento]["Magnitud"])+self.Unidades["UMomentos"],(regla_de_3(self.LenBarra,posicion)+3, int(largo_y/2) -25), font, 0.5, (0,0,0),1,cv2.LINE_AA)

            else: #↷   
                startAngle = 0
                endAngle = -270

                cv2.arrowedLine(imagen, (regla_de_3(self.LenBarra,posicion)-1, int(largo_y/2) +25), (regla_de_3(self.LenBarra,posicion), int(largo_y/2) +25), (0,0,0), 2, tipLength = 10)                    
                cv2.putText(imagen,str(Momentos[momento]["Magnitud"])+self.Unidades["UMomentos"],(regla_de_3(self.LenBarra,posicion)+3, int(largo_y/2) +25), font, 0.5, (0,0,0),1,cv2.LINE_AA)

            cv2.ellipse(imagen, center_coordinates, axesLength, angle, startAngle, endAngle, color, thickness)

    dibujar_soportes(self.Soportes)
    dibujar_cargas_puntuales(self.CargasPuntuales)
    dibujar_cargas_distribuidas(self.CargasDistribuidas)
    dibujar_momentos(self.Momentos)
    
    #Acotar
    org_cotas(self.Cotas,imagen,self.LenBarra,self.Unidades["ULong"])
    return imagen

# Regla de tres entre la longitud de la barra y los pixeles
def regla_de_3(longitud_barra,longitud):
    pixel_posicion=((longitud*(max_x-min_x))/longitud_barra)+(min_x)
    return int(round(pixel_posicion,0))

#Convierte desde una magnitud cualquiera a su punto en pixeles
def conversion(magnitud,Vm): 
    m = (largo_y/(3*Vm)) if Vm != 0 else 0 #Pendiente

    return int(m*magnitud + largo_y/2)

#  dibuja las lineas de acotación
def acotar(imagen,unidad,inicio,final,unidad_long):
    #Cotas horizontales
    cv2.line(imagen, (int(((final+inicio)/2)-30),largo_y-10), (inicio,largo_y-10), (0,0,0), 1)
    cv2.line(imagen, (int(((final+inicio)/2)+30),largo_y-10), (final,largo_y-10), (0,0,0), 1)
    #flechas de acotacion
    cv2.line(imagen, (inicio,largo_y-10), (inicio+5,largo_y-13), (0,0,0), 1) #Der Arriba
    cv2.line(imagen, (inicio,largo_y-10), (inicio+5,largo_y-7), (0,0,0), 1) #Der Abajo
    cv2.line(imagen, (final,largo_y-10), (final-5,largo_y-13), (0,0,0), 1) #Izq Arriba
    cv2.line(imagen, (final,largo_y-10), (final-5,largo_y-7), (0,0,0), 1) #Izq Abajo
    #unidad
    if len(str(unidad))>3: unidad=round(unidad,2) 
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(imagen,str(unidad)+unidad_long,(int(((final+inicio)/2)-10*(len(str(unidad))+1)/2),largo_y-10),font,0.5,(0,0,0),1,cv2.LINE_AA)

# organizacion de las cotas para dibujar
def org_cotas(cotas,imagen,longitud_barra,unidad_long):
    for i in range(len(cotas)):
        if i == len(cotas)-1: break
        acotar(imagen,cotas[i+1]-cotas[i],regla_de_3(longitud_barra,cotas[i]),regla_de_3(longitud_barra,cotas[i+1]),unidad_long)

#Actualiza las cotas del modelo
def actualiza_cotas(self):
    cotas = [0,self.LenBarra]
    
    #Actualiza cotas de los soportes
    for key, value in self.Soportes.items():
        if type(key) == str or len(value) == 0: continue
        for posicion in value:
            cotas.append(posicion)

    #Actualiza cotas de las cargas puntuales
    for key, value in self.CargasPuntuales.items():
        cotas.append(value["Posicion"])

    #Actualiza cotas de las cargas distribuidas
    for key, value in self.CargasDistribuidas.items():
        cotas.append(value["Posiciones"][0])
        cotas.append(value["Posiciones"][1])
    
    #Actualiza cotas de los momentos
    for key, value in self.Momentos.items():
        cotas.append(value["Posicion"])

    #Depurar cotas
    cotas = sorted(list(set(cotas)))
    return cotas
    
# Crea la imagen con la barra incluida
def crear_imagen():
    # Crear la imagen en blanco
    imagen = 255*np.ones((int(largo_y),int(largo_x),3),dtype=np.uint8)
    # Dibuja la barra 
    cv2.line(imagen,(min_x,int(largo_y/2)),(max_x,int(largo_y/2)),(255,0,0),5)
    # Colocar coordenadas
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.line(imagen,(min_x,max_y+int(min_y*(1/3))),(min_x,min_y-int(min_y*(1/3))),(0,0,0),1) #Eje y
    cv2.putText(imagen,"y",(min_x,int(min_y/2)),font,1,(0,0,0),1,cv2.LINE_AA)
    cv2.line(imagen,(min_x-int(min_x*(1/3)),int(largo_y/2)),(max_x+int(min_x*(1/3)),int(largo_y/2)),(0,0,0),1) #Eje x
    cv2.putText(imagen,"x",(max_x+int(min_x/2),int(largo_y/2)),font,1,(0,0,0),1,cv2.LINE_AA)
    return imagen

# Muestra las imagenes
def mostrar_imagen(imagen,nombre):
    cv2.imshow(nombre,imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#**************************************Resolver********************************************
#Devuelve el valores utiles de cada soporte (Formula el resultado paso por paso mostrandolo en pantalla)
def valor_soportes(self):
    borrarPantalla()
    #Determinar la viablididad del procedimiento
    if self.Soportes["Total"] != 2: 
        _except(3,"Hacen falta soportes en el modelo.")
        return


    #*******************************************Creacion de ecuaciones/Soportes*************************************
    #Soportes tipo 3
    if len(self.Soportes[3])!=0:
        #Incognitas
        S_x, S_y, SM = symbols("S_x S_y SM") #Donde S_x se refiere a la incognita en x del soporte, S_y es la incognita en y, y SM es la incognita de momentos 
        incognitas = (S_y, SM) 
        
        #Creacion de ecuaciones
        ec_x = S_x
        ec_y = S_y
        ec_momentos = SM + S_y*self.Soportes[3][0] #Lo resuelve en base a la posicion 0
        
    #Soportes tipo 1 y 2
    else:
        soportes_dict = {}
        #Incognitas
        S1_x, S1_y, S2_x, S2_y = symbols("S1_x S1_y S2_x S2_y") #Donde S1 se refiere a un primer soporte y de igual modo S2  
        incognitas = (S1_y, S2_y) 

        #Creacion de ecuaciones
        ec_momentos = 0 #Lo resuelve en base a la posicion 0
        
        #Elaboracion de ecuaciones
        indicador = 1
        for i in range(1,3):
            if len(self.Soportes[i]) == 0: continue
            
            for posicion_soporte in self.Soportes[i]:
                if i == 2 and indicador == 1: S1_x = 0
                elif i == 2 and indicador == 2: S2_x = 0

                soportes_dict["S"+str(indicador)] = {"Tipo": i, "Posicion": posicion_soporte}
                
                ec_momentos = ec_momentos + (S1_y if indicador == 1 else S2_y)*posicion_soporte    
                indicador += 1
        #Llenados
        ec_x = S1_x + S2_x
        ec_y = S1_y + S2_y
        del indicador


    #**************************************************Momentos******************************************************
    for i in range(1,len(self.Momentos)+1):
        if self.Momentos[i]["Direccion"] != 1: 
            ec_momentos = Add(ec_momentos, Mul(Integer(-1), self.Momentos[i]["Magnitud"], evaluate=False), evaluate=False)
        else: 
            ec_momentos = Add(ec_momentos, self.Momentos[i]["Magnitud"], evaluate=False)


    #***********************************************Cargas Puntuales************************************************
    for i in range(1,len(self.CargasPuntuales)+1):            
        if self.CargasPuntuales[i]["Direccion"] != 1: 
            ec_y = Add(ec_y, Mul(Integer(-1), self.CargasPuntuales[i]["Magnitud"], evaluate = False), evaluate=False)
            ec_momentos = Add(ec_momentos, Mul(Integer(-1), self.CargasPuntuales[i]["Magnitud"], self.CargasPuntuales[i]["Posicion"], evaluate=False), evaluate=False)
        else: 
            ec_y = Add(ec_y, self.CargasPuntuales[i]["Magnitud"], evaluate=False)
            ec_momentos = Add(ec_momentos, Mul(self.CargasPuntuales[i]["Magnitud"], self.CargasPuntuales[i]["Posicion"], evaluate=False), evaluate=False)


    #***********************************************Cargas Distribuidas*****************************************************
    for i in range(1,len(self.CargasDistribuidas)+1):
        m_1, m_2 = self.CargasDistribuidas[i]["Magnitudes"]
        p_1, p_2 = self.CargasDistribuidas[i]["Posiciones"]
        
        # area
        area=cd_area(m_1, m_2, p_1, p_2)
        # centroides
        centroide_x=cd_centroide(m_1, m_2, p_1, p_2)

        
        if self.CargasDistribuidas[i]["Direccion"] != 1: 
            ec_y = Add(ec_y, Mul(Integer(-1), area, evaluate=False), evaluate=False)
            ec_momentos = Add(ec_momentos, Mul(Integer(-1), area, centroide_x, evaluate=False), evaluate=False)
        else: 
            ec_y = Add(ec_y, area, evaluate=False)
            ec_momentos = Add(ec_momentos, Mul(area, centroide_x, evaluate=False), evaluate=False)

        
    #**********************************************Resolver ecuaciones*******************************************************+
    init_printing(use_unicode=True)

    #Pone bonito la ecuacion ec_momentos para mostrar:        
    ec_momentos_str = str(ec_momentos).replace("+ (-1)*","- ") 
    ec_y_str = str(ec_y).replace("+ (-1)*","- ") 

    #Imprime las ecuaciones
    print(f"""Ecuaciones: \nFuerzas en eje X = 0 \n{ec_x} = 0 \n\nFuerzas en eje Y = 0 \n{ec_y_str} = 0 \n\nMomentos(x = 0) = 0 \n{ec_momentos_str} = 0""")
    
    ec_y, ec_momentos = simplify(ec_y), simplify(ec_momentos)
    result, = (linsolve([ec_y, ec_momentos], incognitas))
    
    #Resolver con protocolo soporte tipo 3
    if len(self.Soportes[3]) != 0:
        print(f"""\n\nSolucionando: \nS_x = 0 (Componente de Fuerza_X del soporte)\nS_y = {round(result[0],3)}{self.Unidades["UCarga"]} (Componente de Fuerza_Y del soporte)\nSM = {round(result[1],3)}{self.Unidades["UMomentos"]} (Componente de momento del soporte)""")
        valores = {"S_y": result[0], "SM": result[1]} #Valores que se retornan

    #Resolver para soportes 1 y 2
    else:
        Fx_S1 = solve(ec_x, S1_x)
        Fx_S2 = solve(ec_x, S2_x)

        print(f"""\n\nSolucionando para el soporte S1: Tipo = {soportes_dict["S1"]["Tipo"]}, Posicion = {soportes_dict["S1"]["Posicion"]}: \nS1_x = {Fx_S1} (Componente de Fuerza_X del soporte) \nS1_y = {round(result[0],3)}{self.Unidades["UCarga"]} (Componente de Fuerza_Y del soporte)""")
        print(f"""\nSolucionando para el soporte S2: Tipo = {soportes_dict["S2"]["Tipo"]}, Posicion = {soportes_dict["S2"]["Posicion"]}: \nS2_x = {Fx_S2} (Componente de Fuerza_X del soporte) \nS2_y = {round(result[1],3)}{self.Unidades["UCarga"]} (Componente de Fuerza_Y del soporte)""")
        valores = {soportes_dict["S1"]["Posicion"]: result[0], soportes_dict["S2"]["Posicion"]: result[1]} #Valores que se retornan


    try: input("\n\nPresione cualquier tecla para continuar... ")
    except: _except("3")

    return valores

#Funcion que devuelve la funcion de carga de la barra en array 
class funcion_carga:
    def __init__(self, modelo):
        self.CargasPuntualesGenerales = modelo.CargasPuntualesGenerales
        self.CargasDistribuidas = modelo.CargasDistribuidas
        self.Cotas = modelo.Cotas
        self.LenBarra = modelo.LenBarra

    #Funcion dada una posicion
    def __funcion_carga_posicion__(self,valor:float):
        ec = 0

        #Magnitud final de una carga distribuida con un x intermedio entre p_2 y p_1 de la carga distribuida
        def m_f_CD(m_1, m_2_final, p_1, p_2_final):
            m = (m_2_final-m_1)/(p_2_final - p_1)
            b = m_1 - m*p_1
            return m*x + b

        #Añadir valores puntuales
        for key, value in self.CargasPuntualesGenerales.items():
            if value["Posicion"] < valor: ec = ec + (value["Magnitud"] * (-1 if value["Direccion"] != 1 else 1)) 

        #Añadir valores distribuidos
        for key, value in self.CargasDistribuidas.items():
            m_1, m_2 = value["Magnitudes"]
            p_1, p_2 = value["Posiciones"]
            
            # area
            area=cd_area(m_1, m_2, p_1, p_2)

            if p_2 < valor: ec = ec + (area * (-1 if value["Direccion"] != 1 else 1))
            elif valor > p_1 and valor <= p_2: ec = ec + (cd_area(m_1, m_f_CD(m_1,m_2,p_1,p_2), p_1, x) * (-1 if value["Direccion"] != 1 else 1))

        return simplify(ec)

    #Aglomerado de funciones
    def f_sympy(self):
        """Devuelve una lista con diccionarios que describen el comportamiento de la funcion de carga"""       
        
        f_carga = []
        for i in range(len(self.Cotas)-1):
            rang_ini, rang_fin = self.Cotas[i], self.Cotas[i+1]
            f_carga.append({"rang_ini": rang_ini, "rang_fin": rang_fin, "funcion": self.__funcion_carga_posicion__(rang_fin)})
        return f_carga

    #Funcion hecho array
    def f_array(self):
        #Elaboracion del array
        f = np.array([]) #Array
        for i in range(len(self.Cotas)):
            if i == len(self.Cotas)-1: break
            #Acomodo de las iteraciones
            if (i == len(self.Cotas)-2): iteraciones = max_x-min_x - np.shape(f)[0] 
            else: iteraciones = regla_de_3(self.LenBarra,self.Cotas[i+1]-self.Cotas[i])-min_x
    
            funcion_momentanea = funcion_array((self.Cotas[i],self.Cotas[i+1]), iteraciones, self.__funcion_carga_posicion__(self.Cotas[i+1]))
            f = np.concatenate((f, funcion_momentanea))
        return f

    #Maximo y minimo de la funcion de carga
    def extremos(self):
        #Depurar las posiciones repetidas
        def comprobar_posiciones(posiciones):
            posiciones_copy = []
            posiciones_no_repetibles = [] 
            for posicion in posiciones:
                if type(posicion) == str:
                    pos_1, pos_2 = posicion[0:posicion.find("<=")], posicion[posicion.find("<= x <=")+8::]
                    posiciones_no_repetibles.append(round(float(pos_1),5))
                    posiciones_no_repetibles.append(round(float(pos_2),5))

            for posicion in posiciones:
                if type(posicion) == float and posicion in posiciones_no_repetibles: continue
                posiciones_copy.append(posicion)
                posiciones_no_repetibles.append(posicion)
            return posiciones_copy

        MaxCarga, MinCarga = {"magnitud": 0, "posicion": []}, {"magnitud": 0, "posicion": []}
        for funcion_acotada in self.f_sympy():
            f_Carga = Funcion(funcion_acotada["funcion"])
            _max_ = f_Carga.Max(intervalo=(funcion_acotada["rang_ini"], funcion_acotada["rang_fin"]), posicion=True)
            _min_ = f_Carga.Min(intervalo=(funcion_acotada["rang_ini"], funcion_acotada["rang_fin"]), posicion=True)

            if _max_[0] > MaxCarga["magnitud"]: MaxCarga["magnitud"], MaxCarga["posicion"] = _max_[0], _max_[1]
            elif _max_[0] == MaxCarga["magnitud"]:
                for x in _max_[1]: MaxCarga["posicion"].append(x) 

            if _min_[0] < MinCarga["magnitud"]: MinCarga["magnitud"], MinCarga["posicion"] = _min_[0], _min_[1]
            elif _min_[0] == MinCarga["magnitud"]: 
                for x in _min_[1]:  MinCarga["posicion"].append(x) 
        
        MaxCarga["posicion"] = comprobar_posiciones(MaxCarga["posicion"])
        MinCarga["posicion"] = comprobar_posiciones(MinCarga["posicion"])

        if len(MaxCarga["posicion"]) == 1: MaxCarga["posicion"] = MaxCarga["posicion"][0]
        if len(MinCarga["posicion"]) == 1: MinCarga["posicion"] = MinCarga["posicion"][0]

        return {"Max": MaxCarga, "Min":MinCarga}

    #Magnitud de la carga en una posicion de la barra
    def valor(self, posicion):
        for funcion_acotada in self.f_sympy():
            if funcion_acotada["rang_ini"] <= posicion and posicion <= funcion_acotada["rang_fin"]: 
                f = lambdify([x], funcion_acotada["funcion"])
                return f(posicion)

#Grafica de las cargas mediante la funcion carga
def graficas_cargas(self, f_carga, Cotas = None):
    """Que Cotas sea None, quiere decir que se mostrarán todas las cotas de carga, de lo contrario se deberá establecer posición (type list) para mostrar una cotas especifica"""
    #Creacion de la imagen
    imagen_cargas = crear_imagen()
    cv2.putText(imagen_cargas,f"""({self.Unidades["UCarga"]})""",(min_x + 15,int(min_y/2)),font,0.5,(0,0,0),1,cv2.LINE_AA)
    cv2.putText(imagen_cargas,f"""({self.Unidades["ULong"]})""",(max_x+int(min_x/2) + 15,int(largo_y/2)),font,0.5,(0,0,0),1,cv2.LINE_AA)

    #Acotar
    org_cotas(self.Cotas, imagen_cargas, self.LenBarra, self.Unidades["ULong"])

    #Posiciones relevantes pero en pixeles
    cotas_pixel = []
    for x in ((np.array(self.Cotas)*(max_x-min_x))/self.LenBarra)+(min_x): cotas_pixel.append(int(x))

    #Grafica de la funcion de carga
    Vm = -abs(np.amax(f_carga)) if abs(np.amax(f_carga)) > abs(np.amin(f_carga)) else -abs(np.amin(f_carga)) #Valor maximo de la funcion carga
    lista_cotas = [] #Lista con todas las cotas de carga colocadas
    for pixel in range(min_x, max_x):
        cv2.circle(imagen_cargas, (pixel, conversion(f_carga[pixel-min_x], Vm)), 1, (120, 40, 140), 1)
        if pixel != max_x-1: cv2.line(imagen_cargas, (pixel, conversion(f_carga[pixel-min_x], Vm)), (pixel+1, conversion(f_carga[pixel-min_x+1], Vm)), (120, 40, 140), 1)    

        #Dibuja las cotas de los puntos clave
        #Para que se muestra una cota carga, el pixel debe estar entre las cotas relvantes o ser el ultimo pixel, además deberá ser la primera vez que se imprime esta cota y no ser 0
        if (pixel in cotas_pixel or pixel == max_x-1) and (round(f_carga[pixel-min_x], 2) not in lista_cotas) and (f_carga[pixel-min_x] != 0) and (Cotas == None): 
            cv2.putText(imagen_cargas, str(round(f_carga[pixel-min_x], 2)) + self.Unidades["UCarga"], (pixel+10, conversion(f_carga[pixel-min_x], Vm)+10), font, 0.3, (0,0,0), 1, cv2.LINE_AA)
            lista_cotas.append(round(f_carga[pixel-min_x], 2))
    
    #acotar cargas en Cotas
    if Cotas != None:
        print("")
        for posicion in Cotas:
            cota_carga = funcion_carga(self).valor(posicion)
            cv2.line(imagen_cargas, (regla_de_3(self.LenBarra,posicion), int(largo_y/2)), (regla_de_3(self.LenBarra,posicion), conversion(cota_carga, Vm)), (0,0,0), 1)
            cv2.line(imagen_cargas, (min_x, conversion(cota_carga, Vm)), (regla_de_3(self.LenBarra,posicion), conversion(cota_carga, Vm)), (0,0,0), 1)
            cv2.putText(imagen_cargas, str(round(cota_carga, 2)) + self.Unidades["UCarga"], (min_x-50, conversion(cota_carga, Vm)), font, 0.3, (0,0,0), 1, cv2.LINE_AA)
            print(f"""f({posicion}{self.Unidades["ULong"]}) = {cota_carga}{self.Unidades["UCarga"]}""")

    #Lineas del principio y el final
    cv2.line(imagen_cargas, (min_x, int(largo_y/2)), (min_x, conversion(f_carga[0], Vm)), (120, 40, 140), 1)    
    cv2.line(imagen_cargas, (max_x, int(largo_y/2)), (max_x, conversion(f_carga[-1], Vm)), (120, 40, 140), 1)    

    #Mostrar imagen
    mostrar_imagen(imagen_cargas, "Fuerza Cortante :3")


#Funcion que devuelve la funcion de momentos de la barra en array 
class funcion_momentos:
    def __init__(self, modelo):
        self.CargasPuntualesGenerales = modelo.CargasPuntualesGenerales
        self.MomentosGenerales = modelo.MomentosGenerales
        self.CargasDistribuidas = modelo.CargasDistribuidas
        self.Cotas = modelo.Cotas
        self.LenBarra = modelo.LenBarra

    #Funcion que devuelve la funcion de momentos correspondiente a una posicion de la barra
    def __funcion_momento_posicion__(self, valor:float):
        ec = 0

        #Magnitud final de una carga dsitribuida con un x intermedio entre p_2 y p_1 de la carga distribuida
        def m_f_CD(m_1, m_2_final, p_1, p_2_final):
            m = (m_2_final - m_1)/(p_2_final - p_1)
            b = m_1 - m*p_1
            return m*x + b

        #Añadir valores puntuales (cargas puntuales y momentos)
        for key, value in self.CargasPuntualesGenerales.items():
            if value["Posicion"] < valor: ec = ec + ((value["Magnitud"] * (x - value["Posicion"])) * (1 if value["Direccion"] != 1 else -1)) 

        for key, value in self.MomentosGenerales.items():
            if value["Posicion"] < valor: ec = ec + (value["Magnitud"] * (-1 if value["Direccion"] != 1 else 1)) 

        #Añadir valores distribuidos
        for key, value in self.CargasDistribuidas.items():
            m_1, m_2 = value["Magnitudes"]
            p_1, p_2 = value["Posiciones"]
            
            if p_2 < valor: 
                area, centroide = cd_area(m_1, m_2, p_1, p_2), cd_centroide(m_1, m_2, p_1, p_2)
                ec = ec + ((area * (x - centroide)) * (1 if value["Direccion"] != 1 else -1))

            elif valor > p_1 and valor <= p_2: 
                area, centroide = cd_area(m_1, m_f_CD(m_1,m_2,p_1,p_2), p_1, x), cd_centroide(m_1, m_f_CD(m_1,m_2,p_1,p_2), p_1, x)
                ec = ec + ((area * (x - centroide)) * (1 if value["Direccion"] != 1 else -1))

        return simplify(-ec)

    #Aglomerado de funciones
    def f_sympy(self):
        """Devuelve una lista con diccionarios que describen el comportamiento de la funcion de momentos"""       
        
        f_carga = []
        for i in range(len(self.Cotas)-1):
            rang_ini, rang_fin = self.Cotas[i], self.Cotas[i+1]
            f_carga.append({"rang_ini": rang_ini, "rang_fin": rang_fin, "funcion": self.__funcion_momento_posicion__(rang_fin)})
        return f_carga

    #Funcion hecho array
    def f_array(self):
        #Elaboracion del array
        M = np.array([]) #Array
        for i in range(len(self.Cotas)):
            if i == len(self.Cotas)-1: break
            #Acomodo de las iteraciones
            if (i == len(self.Cotas)-2): iteraciones = max_x-min_x - np.shape(M)[0] 
            else: iteraciones = regla_de_3(self.LenBarra,self.Cotas[i+1]-self.Cotas[i])-min_x
    
            funcion_acotada = funcion_array((self.Cotas[i],self.Cotas[i+1]), iteraciones, self.__funcion_momento_posicion__(self.Cotas[i+1]))
            M = np.concatenate((M, funcion_acotada))
        
        return M

    #Maximo y minimo de la funcion de momento
    def extremos(self):
        #Depurar las posiciones repetidas
        def comprobar_posiciones(posiciones):
            posiciones_copy = []
            posiciones_no_repetibles = [] 
            for posicion in posiciones:
                if type(posicion) == str:
                    pos_1, pos_2 = posicion[0:posicion.find("<=")], posicion[posicion.find("<= x <=")+8::]
                    posiciones_no_repetibles.append(round(float(pos_1),5))
                    posiciones_no_repetibles.append(round(float(pos_2),5))

            for posicion in posiciones:
                if type(posicion) == float and posicion in posiciones_no_repetibles: continue
                posiciones_copy.append(posicion)
                posiciones_no_repetibles.append(posicion)

            return posiciones_copy
 
        MaxMomento, MinMomento = {"magnitud": 0, "posicion": []}, {"magnitud": 0, "posicion": []}
        for funcion_acotada in self.f_sympy():
            f_Momento = Funcion(funcion_acotada["funcion"])
            _max_ = f_Momento.Max(intervalo=(funcion_acotada["rang_ini"], funcion_acotada["rang_fin"]), posicion=True)
            _min_ = f_Momento.Min(intervalo=(funcion_acotada["rang_ini"], funcion_acotada["rang_fin"]), posicion=True)

            if _max_[0] > MaxMomento["magnitud"]: MaxMomento["magnitud"], MaxMomento["posicion"] = _max_[0], _max_[1]
            elif _max_[0] == MaxMomento["magnitud"]:
                for x in _max_[1]: MaxMomento["posicion"].append(x) 

            if _min_[0] < MinMomento["magnitud"]: MinMomento["magnitud"], MinMomento["posicion"] = _min_[0], _min_[1]
            elif _min_[0] == MinMomento["magnitud"]: 
                for x in _min_[1]:  MinMomento["posicion"].append(x) 

        MaxMomento["posicion"] = comprobar_posiciones(MaxMomento["posicion"])
        MinMomento["posicion"] = comprobar_posiciones(MinMomento["posicion"])

        if len(MaxMomento["posicion"]) == 1: MaxMomento["posicion"] = MaxMomento["posicion"][0]
        if len(MinMomento["posicion"]) == 1: MinMomento["posicion"] = MinMomento["posicion"][0]
        return {"Max": MaxMomento, "Min":MinMomento}

    #Magnitud del momento en una posicion de la barra
    def valor(self, posicion):
        for funcion_acotada in self.f_sympy():
            if funcion_acotada["rang_ini"] <= posicion and posicion <= funcion_acotada["rang_fin"]: 
                f = lambdify([x], funcion_acotada["funcion"])
                return f(posicion)

#Grafica de las momentos mediante la funcion momentos
def graficas_momentos(self, f_momentos, Cotas = None):
    """Que Cotas sea None, quiere decir que se mostrarán todas las cotas de carga, de lo contrario se deberá establecer posición (type list) para mostrar una cotas especifica"""
    #Creacion de la imagen
    imagen_momentos = crear_imagen()
    cv2.putText(imagen_momentos,f"""({self.Unidades["UMomentos"]})""",(min_x + 15,int(min_y/2)),font,0.5,(0,0,0),1,cv2.LINE_AA)
    cv2.putText(imagen_momentos,f"""({self.Unidades["ULong"]})""",(max_x+int(min_x/2) + 15,int(largo_y/2)),font,0.5,(0,0,0),1,cv2.LINE_AA)

    #Acotar
    org_cotas(self.Cotas, imagen_momentos, self.LenBarra, self.Unidades["ULong"])

    #Posiciones relevantes pero en pixeles
    cotas_pixel = []
    for x in ((np.array(self.Cotas)*(max_x-min_x))/self.LenBarra)+(min_x): cotas_pixel.append(int(x))

    #Grafica de la funcion de momentos
    Vm = -abs(np.amax(f_momentos)) if abs(np.amax(f_momentos)) > abs(np.amin(f_momentos)) else -abs(np.amin(f_momentos)) #Valor maximo de la funcion momento
    lista_cotas = [] #Lista con todas las cotas de momentos colocadas
    for pixel in range(min_x, max_x):
        cv2.circle(imagen_momentos, (pixel, conversion(f_momentos[pixel-min_x], Vm)), 1, (120, 40, 140), 1)
        if pixel != max_x-1: cv2.line(imagen_momentos, (pixel, conversion(f_momentos[pixel-min_x], Vm)), (pixel+1, conversion(f_momentos[pixel-min_x+1], Vm)), (120, 40, 140), 1)    

        #Dibuja las cotas de los puntos clave
        #Para que se muestra una cota momentos, el pixel debe estar entre las cotas relvantes o ser el ultimo pixel, además deberá ser la primera vez que se imprime esta cota y no ser 0
        if (pixel in cotas_pixel or pixel == max_x-1) and (round(f_momentos[pixel-min_x], 2) not in lista_cotas) and (f_momentos[pixel-min_x] != 0) and (Cotas == None): 
            cv2.putText(imagen_momentos, str(round(f_momentos[pixel-min_x], 2)) + self.Unidades["UCarga"], (pixel+10, conversion(f_momentos[pixel-min_x], Vm)+10), font, 0.3, (0,0,0), 1, cv2.LINE_AA)
            lista_cotas.append(round(f_momentos[pixel-min_x], 2))
    
    #acotar momentos en Cotas
    if Cotas != None:
        print("")
        for posicion in Cotas:
            cota_momentos = funcion_momentos(self).valor(posicion)
            cv2.line(imagen_momentos, (regla_de_3(self.LenBarra,posicion), int(largo_y/2)), (regla_de_3(self.LenBarra,posicion), conversion(cota_momentos, Vm)), (0,0,0), 1)
            cv2.line(imagen_momentos, (min_x, conversion(cota_momentos, Vm)), (regla_de_3(self.LenBarra,posicion), conversion(cota_momentos, Vm)), (0,0,0), 1)
            cv2.putText(imagen_momentos, str(round(cota_momentos, 2)) + self.Unidades["UMomentos"], (min_x-50, conversion(cota_momentos, Vm)), font, 0.3, (0,0,0), 1, cv2.LINE_AA)
            print(f"""f({posicion}{self.Unidades["ULong"]}) = {cota_momentos}{self.Unidades["UMomentos"]}""")

    #Lineas del principio y el final
    cv2.line(imagen_momentos, (min_x, int(largo_y/2)), (min_x, conversion(f_momentos[0], Vm)), (120, 40, 140), 1)    
    cv2.line(imagen_momentos, (max_x, int(largo_y/2)), (max_x, conversion(f_momentos[-1], Vm)), (120, 40, 140), 1)    

    #Mostrar imagen
    mostrar_imagen(imagen_momentos, "Momento Flector :3")

