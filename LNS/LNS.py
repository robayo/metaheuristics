# Le 26 Novembre 2020
from time import perf_counter
from os import listdir
import random
from os.path import isfile, join
from itertools import combinations
import operator
import copy
import math


class PDPTW:
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, [sum(i[-1]) for i in self.distancia_actual])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, [sum(i[-1]) for i in self.distancia_actual])

    '''
    Inicializo la clase problemas.
    Input: path del archivo de datos de la instancia 
    '''

    def __init__(self, file_name):
        self.FOS = []
        self.MDistancias = []  # Matriz de distancia l[nodoa][nodob]
        self.VEHICULOS, self.CAPACIDAD, self.SPEED = 0, 0, 0
        self.demanda = []
        self.minima_distancia = {}
        self.distancias = dict()
        self.lim_inferior = []
        self.lim_superior = []
        self.tiempo_servicio = []
        self.nodos_pickup = dict()
        self.nodos_delivery = dict()
        self.ordenes = dict()  # Diccionario con keys de los pares nodo (pickup, delivery) y demanda positiva como valor.
        self.coordenadas = []  # vector de tuplas (x,y)
        self.get_data(file_name)
        self.rutas = []  # Vector de vectores: Alberga en cada vector la sucesión de nodos que visita la ruta
        self.distancia_actual = []  # Vector de vectores: Alberga en cada vector la distancia recorrida al salir del nodo
        self.tiempo_actual = []  # Vector de vectores: Alberga en cada vector el tiempo al salir del nodo
        self.carga_actual = []  # Vector de vectores: Alberga en cada vector la carga en el camión al salir del nodo
        self.calcular_matriz_distancias()

    def calcular_matriz_distancias(self):
        for i in range(len(self.demanda)):
            self.MDistancias.append([self.calcular_distancia(i, j) for j in range(len(self.demanda))])

    def get_data(self, file_name):
        handle = open(file_name)
        self.VEHICULOS, self.CAPACIDAD, self.SPEED = map(int, next(handle).split())
        for task in handle:
            task_number, x, y, demanda, lim_inferior, lim_superior, tiempo_servicio, pickup, delivery = \
                map(int, task.split())
            self.demanda.append(demanda)
            self.lim_inferior.append(lim_inferior)
            self.lim_superior.append(lim_superior)
            self.coordenadas.append((x, y))
            self.tiempo_servicio.append(tiempo_servicio)
            if pickup == 0:
                self.ordenes[(task_number, delivery)] = demanda
                self.nodos_pickup[task_number] = delivery
            else:
                self.nodos_delivery[task_number] = pickup
        handle.close()
        self.ordenes.pop((0, 0))

    def calcular_distancia(self, nodoA, nodoB):
        if (nodoA, nodoB) not in self.distancias:
            xi, yi = self.coordenadas[nodoA]
            xj, yj = self.coordenadas[nodoB]
            self.distancias[(nodoA, nodoB)] = math.sqrt(math.pow(xi - xj, 2) + math.pow(yi - yj, 2))
        return self.distancias[(nodoA, nodoB)]

    def calcular_minima_distancia(self, orden):
        if orden not in self.minima_distancia:
            self.minima_distancia[orden] = self.MDistancias[0][orden[0]] + self.MDistancias[orden[0]][orden[1]] + \
                                           self.MDistancias[orden[1]][0]
        return self.minima_distancia[orden]

    '''
    Chequea factibilidades unicamente de tiempo y carga,
     no posiciones pickup y delivery '''

    def check_factibilidad(self, vector):
        if not vector: return -float("inf"), [], [], [], vector
        factible = True
        distancias_actual = []
        tiempo_actual = []
        carga_actual = []
        nodo_anterior = 0
        for posicion, nodo in enumerate(vector):
            if not factible: break
            if posicion == 0:
                distancias_actual.append(self.MDistancias[0][nodo])
                tiempo_actual.append(
                    max(self.MDistancias[0][nodo], self.lim_inferior[nodo]) + self.tiempo_servicio[nodo])
                carga_actual.append(self.demanda[nodo])
            else:
                distancias_actual.append(distancias_actual[-1] + self.MDistancias[nodo_anterior][nodo])
                tiempo_llegada_nodo = max(tiempo_actual[-1] + self.MDistancias[nodo_anterior][nodo],
                                          self.lim_inferior[nodo])
                carga_actual.append(carga_actual[-1] + self.demanda[nodo])
                if carga_actual[-1] > self.CAPACIDAD:
                    factible = False
                    pass

                if tiempo_llegada_nodo > self.lim_superior[nodo]:
                    factible = False
                    pass
                else:
                    tiempo_actual.append(tiempo_llegada_nodo + self.tiempo_servicio[nodo])
            nodo_anterior = nodo

        FO = distancias_actual[-1] + self.MDistancias[nodo][0]
        tiempo_total = tiempo_actual[-1] + self.MDistancias[nodo][0]
        if tiempo_total > self.lim_superior[0]:
            factible = False
            pass

        if not factible:
            return None, None, None, None, None
        else:
            return FO, distancias_actual, tiempo_actual, carga_actual, vector

    def greedy_heuristic(self, ordenes_sin_asignar, solucion, FuncionesObjetivo):
        posibles_posiciones = {}
        for pickup, delivery in ordenes_sin_asignar:
            for num_ruta, vector_ruta in enumerate(solucion[0]):
                for posicionA, posicionB in combinations(range(len(vector_ruta) + 2), 2):
                    #vale la pena la combinacion
                    #posicionA
                    if posicionA != 0:
                        tiempoanterior = solucion[2][num_ruta][posicionA-1]
                        llegada_nodo = tiempoanterior + self.MDistancias[solucion[0][num_ruta][posicionA-1]][pickup]
                        if llegada_nodo > self.lim_superior[pickup]:
                            break
                        if posicionA +1 == posicionB:
                            tiempo_llegada = max(self.lim_inferior[pickup], llegada_nodo) + self.tiempo_servicio[pickup] + self.MDistancias[pickup][delivery]
                            if tiempo_llegada > self.lim_superior[delivery]:
                                break



                    posible_ruta = list(vector_ruta)  # makes a copy
                    posible_ruta.insert(posicionA, pickup)
                    posible_ruta.insert(posicionB, delivery)
                    datos_ruta = self.check_factibilidad(posible_ruta)  # numruta, solucion
                    if datos_ruta[
                        0] is not None:  # tiene que decir si es factible y luego hay quue calcular (bassado en los 4 links nevos 2 )el aumento en funcion objetivo: distancia
                        # calcular aumento, añadir al set de opciones, sortear por menor y añadir, si vacio entnces crear nueva lista ruta e inicialixarla

                        posibles_posiciones[((pickup, delivery), (num_ruta, posicionA, posicionB))] = (
                        datos_ruta[0] - FuncionesObjetivo[num_ruta], datos_ruta)
        return posibles_posiciones

    def initialSolution(self):

        # Start a new route to insert a “customer pair” taken from the beginning of a customer-pairs list sorted
        # in decreasing order of their combined objective value

        ordenes_sin_asignar = list(self.ordenes.keys())
        ordenes_sin_asignar.sort(key=self.calcular_minima_distancia)
        A, B = ordenes_sin_asignar.pop()
        self.rutas.append([A, B])
        self.carga_actual.append([self.ordenes[(A, B)], 0])
        tiempo_salidaA = max(self.lim_inferior[A], self.MDistancias[0][A]) + self.tiempo_servicio[A]
        tiempo_salidaB = max(self.lim_inferior[B], tiempo_salidaA + self.MDistancias[A][B]) + self.tiempo_servicio[B]
        self.tiempo_actual.append([tiempo_salidaA, tiempo_salidaB])
        self.distancia_actual.append([self.MDistancias[0][A], self.MDistancias[0][A] + self.MDistancias[A][B]])
        Funciones_Objetivo = [self.distancia_actual[-1][-1] + self.MDistancias[B][0]]

        while len(ordenes_sin_asignar) > 0:
            # Remove a customer pair from the sorted customer-pairs list while the list is not empty. After evaluating
            # all feasible posi- tions of all route, insert the newly removed customer pair into the best-fit position
            # of any route which cause the least incre- ment in the combined objective value;
            pickup, delivery = ordenes_sin_asignar.pop()
            solucion = self.rutas, self.distancia_actual, self.tiempo_actual, self.carga_actual
            posibles_posiciones = self.greedy_heuristic({(pickup, delivery)}, solucion, Funciones_Objetivo)
            if not posibles_posiciones:
                # Crear una nueva ruta:
                self.rutas.append([pickup, delivery])
                self.carga_actual.append([self.demanda[pickup], 0])
                tiempo_salidaA = max(self.lim_inferior[pickup], self.MDistancias[0][pickup]) + self.tiempo_servicio[
                    pickup]
                tiempo_salidaB = max(self.lim_inferior[delivery], tiempo_salidaA + self.MDistancias[pickup][delivery]) + \
                                 self.tiempo_servicio[delivery]
                self.tiempo_actual.append([tiempo_salidaA, tiempo_salidaB])
                self.distancia_actual.append(
                    [self.MDistancias[0][pickup], self.MDistancias[0][pickup] + self.MDistancias[pickup][delivery]])
                Funciones_Objetivo.append(self.distancia_actual[-1][-1] + self.MDistancias[delivery][0])
            else:
                (pickup, delivery), (num_ruta, posicionA, posicionB) = \
                min(posibles_posiciones.items(), key=operator.itemgetter(1))[0]
                datos_ruta = posibles_posiciones[(pickup, delivery), (num_ruta, posicionA, posicionB)][1]
                self.rutas[num_ruta] = datos_ruta[4]
                self.distancia_actual[num_ruta] = datos_ruta[1]
                self.tiempo_actual[num_ruta] = datos_ruta[2]
                self.carga_actual[num_ruta] = datos_ruta[3]
                Funciones_Objetivo[num_ruta] = datos_ruta[0]
        self.FOS = Funciones_Objetivo

    def calcular_funcion_objetivo(self, ruta):
        if not ruta: return -float("inf")
        nodo_anterior = 0
        FO = 0
        for nodo in ruta:
            FO += self.MDistancias[nodo_anterior][nodo]
            nodo_anterior = nodo
        FO += self.MDistancias[ruta[-1]][0]
        return FO


    def regret_heuristic(self, solucion, nodos_insertar, FOS):
        for i in range(len(nodos_insertar)):
            posibles_posiciones = {}
            for pickup, delivery in nodos_insertar:
                for num_ruta, ruta in enumerate(solucion[0]):
                    for posicionA, posicionB in combinations(range(len(ruta) + 2), 2):
                        posible_ruta = list(ruta)  # makes a copy
                        posible_ruta.insert(posicionA, pickup)
                        posible_ruta.insert(posicionB, delivery)
                        #calculamos la nueva funcion objetivo.
                        funcion_nueva_ruta = 0
                        nodo_anterior = 0
                        for  nodo in posible_ruta:
                            funcion_nueva_ruta += self.MDistancias[nodo_anterior][nodo]
                            nodo_anterior = nodo
                        funcion_nueva_ruta += self.MDistancias[nodo][0]
                        posibles_posiciones[(num_ruta, (pickup, delivery))] = (funcion_nueva_ruta - FOS[num_ruta], posible_ruta)
            posibles_posiciones = sorted(posibles_posiciones.items(), key=operator.itemgetter(1), reverse = True)     # (key, valor )
            while posibles_posiciones:
                (num_ruta_alterada,  (pickup, delivery)), (cambioFO, posible_ruta)  = posibles_posiciones.pop()
                FO, distancias_actual, tiempo_actual, carga_actual, vector = self.check_factibilidad(posible_ruta)
                if FO is None:
                    continue
                else:
                    solucion[0][num_ruta_alterada] = vector
                    solucion[1][num_ruta_alterada] = distancias_actual
                    solucion[2][num_ruta_alterada] = tiempo_actual
                    solucion[3][num_ruta_alterada] = carga_actual
                    FOS[num_ruta_alterada] = FO
                    break
        return solucion, FOS, posibles_posiciones

    def worst_removal(self, solucion, q, FO_actual):
        rutas = solucion[0]

        ordenes_a_remover = set()
        ruta_a_rehacer = set()
        while q>0:

            cambio_fo = {} # {(num_ruta, nodo_pickup): cambioFO}
            for num_ruta, ruta in enumerate(rutas):
                for pos_pickup, nodo_pickup in enumerate(ruta):
                    if nodo_pickup in self.nodos_pickup:
                        nodo_delivery = self.nodos_pickup[nodo_pickup]
                        pos_nodo_delivery = ruta.index(nodo_delivery)
                        #Calcular FO
                        FO = 0
                        if pos_pickup == 0:
                            FO -= (self.MDistancias[0][nodo_pickup] + self.MDistancias[nodo_pickup][ruta[1]] )
                            FO += self.MDistancias[0][ruta[1]]

                        else:
                            FO -= (self.MDistancias[ruta[pos_pickup-1]][nodo_pickup] +self.MDistancias[nodo_pickup][ruta[pos_pickup+1]] )
                            FO += self.MDistancias[ruta[pos_pickup-1]][ruta[pos_pickup+1]]

                        if pos_nodo_delivery ==len(ruta)-1:
                            FO -= (self.MDistancias[nodo_delivery][0] + self.MDistancias[ruta[pos_nodo_delivery-1]][nodo_delivery] )
                            FO += self.MDistancias[ruta[pos_nodo_delivery-1]][0]
                        else:
                            FO -= (self.MDistancias[ruta[pos_nodo_delivery-1]][nodo_delivery] +self.MDistancias[nodo_delivery][ruta[pos_nodo_delivery+1]] )
                            FO += self.MDistancias[ruta[pos_nodo_delivery-1]][ruta[pos_nodo_delivery+1]]
                        cambio_fo[(num_ruta, (nodo_pickup, nodo_delivery))] = FO
            num_ruta , (pickup, delivery) = max(cambio_fo.items(), key=operator.itemgetter(1))[0]
            ordenes_a_remover.add((pickup, delivery))
            rutas[num_ruta].remove(pickup)
            rutas[num_ruta].remove(delivery)
            ruta_a_rehacer.add(num_ruta)
            q = q-1

            for num_ruta_alterada in ruta_a_rehacer:
                FO, distancias_actual, tiempo_actual, carga_actual, vector = self.check_factibilidad(
                    rutas[num_ruta_alterada])
                solucion[0][num_ruta_alterada] = vector
                solucion[1][num_ruta_alterada] = distancias_actual
                solucion[2][num_ruta_alterada] = tiempo_actual
                solucion[3][num_ruta_alterada] = carga_actual
                FO_actual[num_ruta_alterada] = FO



        return solucion, ordenes_a_remover, FO_actual

    def random_removal(self, solucion, q, FOS):
        ordenes_a_remover = random.sample(list(self.ordenes.keys()), k=q)

        # Buscar y quitar ordenes:
        rutas_alteradas = set()
        for ruta in solucion[0]:
            if len(ruta) <= 2 and (ruta[0], ruta[1]) not in ordenes_a_remover:
                ordenes_a_remover = [(ruta[0], ruta[1])] + ordenes_a_remover
                break
        for orden_sacada in ordenes_a_remover:
            pickup, delivery = orden_sacada
            for num_ruta, ruta in enumerate(solucion[0]):
                if pickup in ruta:
                    ruta.remove(pickup)
                    ruta.remove(delivery)
                    rutas_alteradas.add(num_ruta)
                    break
        for num_ruta_alterada in rutas_alteradas:
            FO, distancias_actual, tiempo_actual, carga_actual, vector = self.check_factibilidad(
                solucion[0][num_ruta_alterada])
            solucion[1][num_ruta_alterada] = distancias_actual
            solucion[2][num_ruta_alterada] = tiempo_actual
            solucion[3][num_ruta_alterada] = carga_actual
            FOS[num_ruta_alterada] =FO

        return solucion, ordenes_a_remover, FOS

    def insert_greedy_heuristic(self, solucion, ordenes_a_incluir):
        FuncionesObjetivo = [self.calcular_funcion_objetivo(ruta) for ruta in solucion[0]]
        while ordenes_a_incluir:
            posibles_posiciones = self.greedy_heuristic(ordenes_a_incluir, solucion, FuncionesObjetivo)

            if not posibles_posiciones:
                # Terrible, toca detenernos
                break
            (pickup, delivery), (num_ruta, posicionA, posicionB) = \
            min(posibles_posiciones.items(), key=operator.itemgetter(1))[0]
            datos_ruta = posibles_posiciones[(pickup, delivery), (num_ruta, posicionA, posicionB)][1]  # FO, solucion
            solucion[0][num_ruta] = datos_ruta[4]
            solucion[1][num_ruta] = datos_ruta[1]
            solucion[2][num_ruta] = datos_ruta[2]
            solucion[3][num_ruta] = datos_ruta[3]
            FuncionesObjetivo[num_ruta] = datos_ruta[0]
            ordenes_a_incluir.remove((pickup, delivery))
            pass
        return solucion, FuncionesObjetivo, ordenes_a_incluir

    def LNS(self, max_iter=80, q=100):
        '''
        In the LNS, a number of b requests is removed from s using one of three removal heuristics proposed in
        Ropke and Pisinger (2006): Shaw, Random, and Worst.
        :param max_iter: Máximo Número de iteraciones
        :return: None
        '''
        iteracion = 1

        while iteracion < max_iter:
            MejorFO = sum(self.FOS)
            FO = list(self.FOS)
            rutas = [list(ruta) for ruta in self.rutas]
            solucion_prospecta = (rutas, self.distancia_actual[:], self.tiempo_actual[:], self.carga_actual[:])

            solucion_prospecta, ordenes_removidas, FO = self.random_removal(solucion_prospecta, q=q, FOS  = FO)
            #solucion_prospecta, ordenes_removidas,  FO = self.worst_removal(solucion_prospecta, q = q, FO_actual = FO )
            solucion_prospecta, FuncionesObjetivo, ordenes_que_faltan  = self.regret_heuristic(solucion_prospecta, ordenes_removidas, FO)
            solucion_prospecta, FuncionesObjetivo, ordenes_que_faltan = self.insert_greedy_heuristic(solucion_prospecta,  ordenes_removidas)
            if ordenes_que_faltan:
                # Aca decidimos si conservamos la solución  y solamente no actualizamos la incunbente o la descartamos
                pass
            else:
                # Revisar si se pudo disminuir una ruta
                for num_ruta, ruta in enumerate(solucion_prospecta[0]):
                    if not ruta:
                        # Eliminar ruta
                        solucion_prospecta[0].pop(num_ruta)
                        solucion_prospecta[1].pop(num_ruta)
                        solucion_prospecta[2].pop(num_ruta)
                        solucion_prospecta[3].pop(num_ruta)
                        FuncionesObjetivo.pop(num_ruta)
                # Criterio de aceptación
                if sum(FuncionesObjetivo) < MejorFO:
                    # Actualizar mejor solución
                    self.rutas, self.distancia_actual, self.tiempo_actual, self.carga_actual = solucion_prospecta
                    # Toca actualizar ADEMAS la FUNCIÓN OBJETIVO
                    self.FOS = FuncionesObjetivo
                else:
                    # No haga nada
                    # Aca iria una aceptación por temperatura similar a Simualted Annealing

                    # Al tener unas solucion que no disminuye la función objetivo
                    pass

            # Aceptar solucion
            iteracion += 1


if __name__ == "__main__":
    handle = open("calibracion.csv", "a")
    dir = "./pdp_100/"
    files = [f for f in listdir(dir) if not f.startswith('.') and isfile(join(dir, f))]
    FOS = []
    random.shuffle(files)
    for file_path in files:
        print(file_path)
        for q in [12]:
            problem = PDPTW(dir + file_path)
            problem.initialSolution()
            problem.LNS(q=q)
            handle.write(file_path + "," + str(q)+ "," + str( len(problem.rutas)) + "," + str(sum(problem.FOS)) + "\n" )
        break

