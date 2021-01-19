# Nicolas Robayo Pardo. Le 12 Decembre 2020 Tarea 4 Metaheuristicas, algoritmo genetico
import random
from os import listdir
from os.path import isfile, join
from sys import argv
from time import perf_counter
class CVRP:
    def __init__(self, filepath):
        self.mejor_solucion = []
        self.mejor_FO = float("inf")
        self.info = {}
        self.coordenadas = []
        self.distancias = []
        self.demanda = []
        self.poblacion = {}
        self.getData(filepath)

    def getData(self, file_name: str):
        handle = open(file_name)
        text, i, RESTO = handle.read().partition("NODE_COORD_SECTION")
        info = {element[0]: element[1].strip() for element in [line.split(" : ") for line in text.strip().split("\n")]}
        coordenadas, i, RESTO = RESTO.partition("DEMAND_SECTION")
        demandas, i, depots = RESTO.partition("DEMAND_SECTION")
        q = filter(None, coordenadas.split("\n"))
        info['DIMENSION'] = int(info['DIMENSION'])
        info['CAPACITY'] = int(info['CAPACITY'])
        k = filter(None, demandas.split("\n"))
        for coord, demanda in zip(q, k):
            nodo, x, y = map(int,coord.split())
            nodo, demanda = map(int,demanda.split())
            self.coordenadas.append((x,y))
            self.demanda.append(demanda)

        for nodoA in range(info['DIMENSION']):
            self.distancias.append([])
            for nodoB in range(info['DIMENSION']):
                if nodoA == nodoB:
                    self.distancias[nodoA].append(float("inf"))
                else:
                    xA, yA = self.coordenadas[nodoA]
                    xB, yB = self.coordenadas[nodoB]
                    distancia = ((xA-xB)**2 + (yA-yB)**2)**(1/2)
                    self.distancias[nodoA].append(distancia)

        handle.close()
        try:
            a,c  = info["COMMENT"][:-1].split("Optimal value: ")
            self.optimo = int(c)
        except:
            a,c  = info["COMMENT"][:-1].split("Best value: ")
            self.optimo = int(c)
        self.info = info

    def calcular_capacidad(self, ruta):
        if not ruta: return 0
        capacidad = 0
        for nodo in ruta:
            capacidad += self.demanda[nodo]
        return capacidad

    def rehacer_ruta(self, rutas_iniciales):
        primer_nodo = rutas_iniciales[0]
        rutas_inicial = [[primer_nodo]]
        capacidad_actual = self.demanda[primer_nodo]
        distancias_actuales = [self.distancias[0][primer_nodo]]
        rutas_iniciales = rutas_iniciales[1:]
        for nodo in rutas_iniciales:
            demanda_nodo = self.demanda[nodo]
            if capacidad_actual + demanda_nodo > self.info["CAPACITY"]:
                distancias_actuales[-1] = distancias_actuales[-1] + self.distancias[rutas_inicial[-1][-1]][0]


                capacidad_actual = demanda_nodo
                rutas_inicial.append([nodo])
                distancias_actuales.append(self.distancias[0][nodo])
                pass
            else:
                capacidad_actual += demanda_nodo
                distancias_actuales[-1] = distancias_actuales[-1] + self.distancias[rutas_inicial[-1][-1]][nodo]
                rutas_inicial[-1].append(nodo)
        #ultimo nodo
        distancias_actuales[-1] = distancias_actuales[-1] + self.distancias[rutas_inicial[-1][-1]][0]

        return rutas_inicial, distancias_actuales

    def poblacion_inicial(self, poblacion ):
        self.gente = poblacion
        self.poblacion = dict()
        for individuo in range(poblacion):
            rutas_iniciales = random.sample(range(1, self.info["DIMENSION"]), k = self.info["DIMENSION"]-1)
            (rutas_inicial, distancias_actuales) = self.rehacer_ruta(rutas_iniciales)
            self.poblacion[100/(sum(distancias_actuales)+random.random())] = (rutas_inicial, distancias_actuales)

            if self.mejor_FO> sum(distancias_actuales):
                self.mejor_solucion = rutas_inicial
                self.mejor_FO = sum(distancias_actuales)

    def calcular_fo_hijo(self, hijo):
        FO = []
        for cromosoma in hijo:

            FO.append(self.calcular_fo(cromosoma))
        return FO

    def calcular_fo(self, ruta):
        if not ruta: return 0
        FO = self.distancias[0][ruta[0]] + self.distancias[ruta[-1]][0]
        for i in range(1,len(ruta)):
            FO += self.distancias[ruta[i-1]][ruta[i]]
        return FO

    def algoritmo_genetico(self, prob_cross = 0.85, prob_mutacion= 0.05, MAX_ITER=3000,BCRC = True):
        from statistics import mean, stdev
        import matplotlib.pyplot as plt
        media = [mean(self.poblacion)]
        desviacion = [stdev(self.poblacion)]



        #Selección ruleta!!!
        for generaciones in range(MAX_ITER):
            nueva_poblacion = dict()
            for ind in range(int(self.gente)):
                posibilidades = list(self.poblacion.keys())
                min_pos = min(self.poblacion.keys())
                solA, solB = random.choices(posibilidades, weights= [i/(min_pos)-1 for i in posibilidades ]     , k = 2)

                if solA == solB: continue
                #crossover_hibrido
                padreA, padreB = self.poblacion[ solA], self.poblacion[ solB]
                if random.random() < prob_cross:
                    if BCRC == True:
                        hijoA, hijoB = self.crossover_BCRC(padreA, padreB)
                    else:
                        hijoA, hijoB = self.partially_map_crossover( padreA, padreB)
                else:
                    hijoA = ([[nodo for nodo in ruta] for ruta in padreA[0] ] , list(padreA[1])  )
                    hijoB = ([[nodo for nodo in ruta] for ruta in padreB[0] ] , list(padreB[1])  )

                #swap mutacion!
                if random.random() < prob_mutacion:
                    self.swap_mutacion(random.choice([hijoA, hijoB]))
                if sum(hijoA[1])<self.mejor_FO:
                    self.mejor_FO = sum(hijoA[1])
                    self.mejor_solucion = hijoA
                elif sum(hijoB[1])<self.mejor_FO:
                    self.mejor_FO = sum(hijoB[1])
                    self.mejor_solucion = hijoB


                nueva_poblacion[100/ (sum(hijoA[1]) +random.random()) ] = hijoA
                nueva_poblacion[100 / (sum(hijoB[1])+random.random())] = hijoB
            #ELITISM REPLACEMENT

            escogidos = random.sample(list(nueva_poblacion), k = self.gente)
            nueva_p = {}
            for nuevo_individuo in escogidos:
                nueva_p.update({nuevo_individuo: nueva_poblacion[nuevo_individuo]})
            self.poblacion = nueva_p

            media.append(mean(self.poblacion))
            desviacion.append(stdev(self.poblacion))

        import math
        plt.errorbar(range(MAX_ITER+1), media, desviacion, linestyle='None', marker='^' )
        yint = range(0, math.ceil(MAX_ITER) + 1)

        #plt.xticks(yint)
        plt.xlabel('Generaciones', fontsize=11)
        plt.ylabel('Fitness', fontsize=11)
        plt.title("Media y Desv. Estandar de Fitness vs Generaciones", fontsize = 16)
        plt.savefig('Simulacion.jpg', dpi = 300)

        plt.show()


    def swap_mutacion(self, hijo):
        numrutaA, numrutaB = random.sample(range(len(hijo[0])), k = 2 )
        copyA = list(hijo[0][numrutaA])
        copyB = list(hijo[0][numrutaB])
        if not copyA or not copyB:return None
        posicionA, posicionB = random.randrange(len(copyA)), random.randrange(len(copyB))
        copyA[posicionA], copyB[posicionB]  = copyB[posicionB], copyA[posicionA]
        #check factibilidad
        if self.calcular_capacidad(copyA) >self.info["CAPACITY"] or self.calcular_capacidad(copyB) >self.info["CAPACITY"]:
            pass
        else:
            #Haga el cambio
            hijo[0][numrutaA] = copyA
            hijo[0][numrutaB] = copyB
            hijo[1][numrutaA] = self.calcular_fo(copyA)
            hijo[1][numrutaB] = self.calcular_fo(copyB)

    def partially_map_crossover(self, hijoA, hijoB):
        string_ruta_1 = [item for sublist in hijoA[0] for item in sublist]
        string_ruta_2 = [item for sublist in hijoB[0] for item in sublist]
        string_ruta_1, string_ruta_2 = cruzar(string_ruta_1, string_ruta_2)

        #Rehacer rutas
        hijoA = self.rehacer_ruta(string_ruta_1)
        hijoB = self.rehacer_ruta(string_ruta_2)
        return hijoA, hijoB

    def crossover_BCRC(self, padreA, padreB):
        rutasA, distA = padreA
        rutasB, distB = padreB
        sel_rutaA, sel_rutaB = random.randrange(0,len(rutasA)), random.randrange(0,len(rutasB))
        nodos_quitarA = set(rutasA[sel_rutaA])
        nodos_quitarB = set(rutasB[sel_rutaB])
        #Quitar nodos de las rutas seleccionadas del otro padre.
        hijoA = [[nodo for nodo in ruta if nodo not in nodos_quitarB ] for ruta in rutasA ]
        hijoB = [[nodo for nodo in ruta if nodo not in nodos_quitarA] for ruta in rutasB]
        # Debemos reintroducir en la mejor posicion uno por uno
        fos = []
        for hijo, nodos_quitar in zip((hijoA, hijoB), (nodos_quitarB, nodos_quitarA)):
            for nodo_introducir in nodos_quitar:
                mejor_fo = float("inf")
                mejor_posicion = None
                demanda_nodo = self.demanda[nodo_introducir]

                for num_ruta, ruta in enumerate(hijo):
                    if self.calcular_capacidad(ruta) + demanda_nodo > self.info["CAPACITY"]: continue
                    for posicion in range(len(ruta)+1):
                        posible_ruta = list(ruta).insert(posicion, nodo_introducir)
                        fo = self.calcular_fo(posible_ruta)
                        if fo < mejor_fo:
                            mejor_fo = fo
                            mejor_posicion = (num_ruta, posicion)

                if mejor_posicion == None:
                    hijoA = ([[nodo for nodo in ruta] for ruta in padreA[0] ] , list(padreA[1])  )
                    hijoB = ([[nodo for nodo in ruta] for ruta in padreB[0] ] , list(padreB[1])  )
                    return hijoA, hijoB
                else:
                    hijo[mejor_posicion[0]].insert(mejor_posicion[1], nodo_introducir)

        return (hijoA, self.calcular_fo_hijo(hijoA)), (hijoB, self.calcular_fo_hijo(hijoB))



##CODIGO ROBADO. Author: Github, mi implmentacion esta en crossover.py la cual no tiene en cuenta la transitividad.
#Desafortundamente no tuve mas tiempo para completarlo.
#https://github.com/damianpirchio/Flowshop-GA/blob/master/metaheuristicas.py
def eliminar_transitividad( lista):
    cambio = False
    seguir = True
    while seguir:
        for i in lista:
            for j in lista:
                if j[0] == i[1]:
                    i[1] = j[1]
                    lista.remove(j)
                    cambio = True
        if cambio:
            seguir = True
            cambio = False
        else:
            seguir = False

def mapear( protochild, lista_m, pos_inicial, pos_final):
    for i in range(len(protochild)):
        if (i < pos_inicial) or (i > pos_final):
            for j in range(len(lista_m)):
                if protochild[i] in lista_m[j]:
                    if protochild[i] == lista_m[j][0]:
                        protochild[i] = lista_m[j][1]
                    else:
                        protochild[i] = lista_m[j][0]
    return protochild

def cruzar( padre1_secuencia, padre2_secuencia):
    lista_respuesta = []
    tamano = len(padre1_secuencia)
    # Genero dos posiciones al azar teniendo en cuenta el tamano del cromo
    pos1 = random.randint(0, tamano)
    pos2 = random.randint(0, tamano)
    if pos1 >= pos2:
        pos_inicial = pos2
        pos_final = pos1
    else:
        pos_inicial = pos1
        pos_final = pos2
    # Intercambio substrings entre los padres
    # ---------------------------------------
    # 1) Armo Substrings
    substring1 = padre1_secuencia[pos_inicial:pos_final + 1]
    substring2 = padre2_secuencia[pos_inicial:pos_final + 1]
    # 2)Armo Protochilds
    padre1_secuencia[pos_inicial:pos_final + 1] = substring2
    padre2_secuencia[pos_inicial:pos_final + 1] = substring1
    # 3)Armo Lista de Mapeo con los substrings
    lista_mapeo = []
    for i in range(len(substring1)):
        # print("Subs 1: ", substring1 )
        # print("Subs 2: ", substring2 )
        lista_mapeo.append([substring1[i], substring2[i]])
        # print("Lista Mapeo: ", lista_mapeo)
        # lista_mapeo = list(flatten(lista_mapeo))
    # 4)Elimino Transitividad de la Lista de Mapeo
    eliminar_transitividad(lista_mapeo)
    # 5)Reemplazo Final con Lista De Mapeo
    sec_hijo1 = mapear(padre1_secuencia, lista_mapeo, pos_inicial,
                            pos_final)
    sec_hijo2 = mapear(padre2_secuencia, lista_mapeo, pos_inicial,
                            pos_final)
    # 6) Creo 2 hijos y les asigno la secuencia
    return sec_hijo1, sec_hijo2

if __name__ == '__main__':

    prob_cross=0.75
    prob_mutacion=0.1
    MAX_ITER=3000
    BCRC = False
    poblacion =150
    file = "./P-n101-k4.vrp"

    t1_init = perf_counter()
    instancia = CVRP(file)
    instancia.poblacion_inicial(poblacion=poblacion)
    instancia.algoritmo_genetico(prob_cross=prob_cross, prob_mutacion=prob_mutacion, MAX_ITER=MAX_ITER,   BCRC = BCRC)
    t1_stop = perf_counter()
    print(instancia.mejor_FO)
    print(int(instancia.mejor_FO)/instancia.optimo-1)






