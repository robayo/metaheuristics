import sys
from random import randint
from priodict import priorityDictionary
from time import perf_counter
# Tarea Nicolas Robayo Pardo
# Metaheuristicas


# import numpy as np
# Using Dijstra implementation by David Eppstein, all atribution to him c) 2002
# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228

ENDING_STRATEGY = 1
RANDOMIZED = True

VERBOSE = False

SHOW_RESULTS = True
args = []
out = None
class Graph:
    """ Graph data structure, undirected by default. """

    def __init__(self, fileName, directed=False):
        self._graph = {}
        self._info = {}
        self._star = []  # Numpy
        self._adjacency = {}
        self._demanda_total = 0
        self._directed = directed
        self._adjacency = {}
        self.getData(fileName)
        # self.createStar()

        self._Dijkstra = {}

    def Dijkstra(self, start, end=None):

        """
        Find shortest paths from the start vertex to all
        vertices nearer than or equal to the end.

        The input graph G is assumed to have the following
        representation: A vertex can be any object that can
        be used as an index into a dictionary.  G is a
        dictionary, indexed by vertices.  For any vertex v,
        G[v] is itself a dictionary, indexed by the neighbors
        of v.  For any edge v->w, G[v][w] is the length of
        the edge.  This is related to the representation in
        <http://www.python.org/doc/essays/graphs.html>
        where Guido van Rossum suggests representing graphs
        as dictionaries mapping vertices to lists of neighbors,
        however dictionaries of edges have many advantages
        over lists: they can store extra information (here,
        the lengths), they support fast existence tests,
        and they allow easy modification of the graph by edge
        insertion and removal.  Such modifications are not
        needed here but are important in other graph algorithms.
        Since dictionaries obey iterator protocol, a graph
        represented as described here could be handed without
        modification to an algorithm using Guido's representation.

        Of course, G and G[v] need not be Python dict objects;
        they can be any other object that obeys dict protocol,
        for instance a wrapper in which vertices are URLs
        and a call to G[v] loads the web page and finds its links.

        The output is a pair (D,P) where D[v] is the distance
        from start to v and P[v] is the predecessor of v along
        the shortest path from s to v.

        Dijkstra's algorithm is only guaranteed to work correctly
        when all edge lengths are positive. This code does not
        verify this property for all edges (only the edges seen
         before the end vertex is reached), but will correctly
        compute shortest paths even for some graphs with negative
        edges, and will raise an exception if it discovers that
        a negative edge has caused it to make a mistake.
        """
        if start in self._Dijkstra:
            if end in self._Dijkstra[start][0]:

                return
            else:
                D = self._Dijkstra[start][0]
                P = self._Dijkstra[start][1]
                Q = self._Dijkstra[start][2]
        else:
            D = {}  # dictionary of final distances
            P = {}  # dictionary of predecessors
            Q = priorityDictionary()  # est.dist. of non-final vert.
            Q[start] = 0

        for v in Q:
            D[v] = Q[v]
            if v == end: break

            for w in self._adjacency[v]:
                vwLength = D[v] + self._adjacency[v][w]
                if w in D:
                    if vwLength < D[w]:
                        raise ValueError("Dijkstra: found better path to already-final vertex")
                elif w not in Q or vwLength < Q[w]:

                    Q[w] = vwLength
                    P[w] = v

        self._Dijkstra[start] = (D, P, Q)

    def shortestPath(self, start, end):
        """
        Find a single shortest path from the given start vertex
        to the given end vertex.
        The input has the same conventions as Dijkstra().
        The output is a list of the vertices in order along
        the shortest path.
        """

        self.Dijkstra(start, end)
        D, P = self._Dijkstra[start][0:2]
        Path = []
        while 1:
            Path.append(end)
            if end == start: break
            end = P[end]
        Path.reverse()
        return Path

    def getDistance(self, start, end):
        self.Dijkstra(start, end)
        return self._Dijkstra[start][0][end]

    def getCost(self, nodeA, nodeB):

        return self._adjacency[nodeA][nodeB]

    def shortestPathtoArc(self, start, arc_destination, withdistance=False):
        othernode = arc_destination[1]
        results = [None] * 2
        for pos, nodo in enumerate(arc_destination):

            path_to = self.shortestPath(start, nodo)

            if path_to[-2] == othernode:
                results[pos] = (self.getDistance(start, nodo)   - self.getCost(nodo, othernode)        , path_to)
            else:
                path_to.append(othernode)
                results[pos] = (self.getDistance(start, nodo) , path_to)

            othernode = nodo
        pos = 0

        if results[0][0] > results[1][0]:
            pos = 1
        if withdistance:
            return results[pos]
        else:
            return results[pos][1]

    # def createStar(self):
    #     self._point = self.puntero(self._star[:, 0])
    #     self._trace = sorted(range(len(self._star[:, 1])), key=lambda k: self._star[k, 1])
    #     self._rpoint = self.puntero(self._star[:, 1], self._trace)

    # Recuperación de datos
    def getData(self, fileName: str):
        handle = open(fileName)

        for line in handle:
            if line.strip()[0] == "(":
                node = tuple(eval(line.lstrip().split("coste")[0].strip()))

                parts = (line.split())

                self._graph[node] = tuple(map(int, (parts[-3::2])))
                self._demanda_total += self._graph[node][1]
                self._adjacency[node[0]][node[1]] = self._graph[node][0]
                if not self._directed:
                    self._adjacency[node[1]][node[0]] = self._graph[node][0]
                # self._star.append(node + tuple(map(int, (parts[-3::2]))))


            else:
                parts = line.split(":")
                try:
                    self._info[parts[0].strip()] = int(parts[1].strip())
                    if parts[0].strip() == "VERTICES":
                        self._adjacency = {ii: {} for ii in range(1, self._info["VERTICES"] + 1)}
                except:
                    pass

        # self._star.sort(key=lambda x: x[0])
        # self._star = np.array(self._star, dtype=None, copy=True, order='K', subok=False, ndmin=0)
        handle.close()

    def puntero(self, forwardstarcolumn, traza=False):
        arreglo = [self._info["ARISTAS_REQ"]] * ((self._info["VERTICES"]))
        arreglo[0] = 0
        arreglo[1] = 0
        if traza == False:
            iterable = range(forwardstarcolumn.shape[0])

        else:
            iterable = traza

        for k in range(2, self._info["VERTICES"]):
            for q, pos in enumerate(iterable):
                if forwardstarcolumn[pos] >= k:
                    arreglo[k] = q
                    break
        return arreglo

    def adyacentes(self, nodo):
        return self._adjacency[nodo].keys()

    def get_demand(self, nodoinicio, nodofinal):
        return self._graph.get((nodoinicio, nodofinal), (0, 0))[1] + self._graph.get((nodofinal, nodoinicio), (0, 0))[1]
    def get_demanda_total(self, lista_nodos):
        return sum([self.get_demand(ii,jj) for ii,jj in lista_nodos])

    class Ruta():
        def __init__(self, capacity, deposit=False):
            self._capacity = capacity

            self._arcos_cubiertos = []
            if deposit == False:
                self._nodes = []
            else:
                self._nodes = [deposit]

        def print_covered_nodes(self):

            print(self._arcos_cubiertos)

        def current_node(self):
            return self._nodes[-1]

        def add_node(self, node):
            if isinstance(node, int):
                self._nodes.append(node)
            else:
                for i in node:
                    self._nodes.append(i)


        def reduce_capacity(self, covered_demand):
            if covered_demand > self._capacity:
                raise ValueError("La capacidad del camión está siendo excedida")
            if covered_demand <= 0:
                raise ValueError("Solo Números Positivos")
            self._capacity -= covered_demand

        def funcion_objetivo(self, costos):
            costo_total = 0
            for i in range(len(self._nodes) - 1):
                costo_total += costos[self._nodes[i]][self._nodes[i + 1]]
            return costo_total
        def get_current_capacity(self):
            return self._capacity

        def __str__(self):
            return '{}({})'.format(self.__class__.__name__, (self._nodes))

        def __repr__(self):
            return '{}({})'.format(self.__class__.__name__, (self._nodes))

    def selectorNode(self, criteria, rute, remainingArcs, random):
        # Returns index of selected node in remaining Arcs depending on rule, if not node was selected then return None
        def criterionNode(criteria):
            if random:
                criteria = randint(0, 5)

            node = rute.current_node()
            arcosPosibles = [(k, l) for k, l in remainingArcs.keys() if
                             (k == node or l == node) and (rute._capacity - remainingArcs[(k, l)] >= 0)]
            if not arcosPosibles:
                return None
            if len(arcosPosibles)==1:
                return arcosPosibles[0]
            if criteria == 4 and rute._capacity >= self._info["CAPACIDAD"] / 2:
                criteria = 3
            elif criteria == 4 and rute._capacity < self._info["CAPACIDAD"] / 2:
                criteria = 2

            if criteria == 0:
                nodesratio = [self._adjacency[i][j] / rute._capacity for i, j in arcosPosibles]
                arcosel = arcosPosibles[min(range(len(nodesratio)), key=lambda i: nodesratio[i])]
            elif criteria == 1:
                nodesratio = [self._adjacency[i][j] / rute._capacity for i, j in arcosPosibles]
                arcosel = arcosPosibles[max(range(len(nodesratio)), key=lambda i: nodesratio[i])]
            elif criteria == 2:
                distancetoDepot = [self.getDistance(j, self._info["DEPOSITO"]) for i, j in arcosPosibles]
                arcosel = arcosPosibles[min(range(len(distancetoDepot)), key=lambda i: distancetoDepot[i]) ]
            elif criteria == 3:
                distancetoDepot = [self.getDistance(j, self._info["DEPOSITO"]) for i, j in arcosPosibles]
                arcosel = arcosPosibles[max(range(len(distancetoDepot)), key=lambda i: distancetoDepot[i]) ]
            elif criteria == 5:
                cost_of_arc = [self.getDistance(i, j) for i, j in arcosPosibles]
                arcosel = arcosPosibles[cost_of_arc.index(max(cost_of_arc))]


            return arcosel

        def back_to_base():
            backtoRoute = self.shortestPath(rute.current_node(), self._info["DEPOSITO"])[1:]
            rute.add_node(backtoRoute)

        def verificador_ruta(cola_ruta):
            n = len(cola_ruta)
            for i in range(1, n-2):
                #Calcular arcos que conecten a i y que no hayan sido atendidos
                arcos_posibles = [(k, l) for k, l in remainingArcs.keys() if
                             (k == cola_ruta[i] or l == cola_ruta[i]) and (rute._capacity - remainingArcs[(k, l)] >= 0)]
                if arcos_posibles:
                    #usamos el arco con mayor demanda atendible
                    arcos_posibles.sort(key= lambda x: remainingArcs[x])       #, reverse = True
                    if arcos_posibles[0][0] == cola_ruta[i]:
                        nuevo_nodo = arcos_posibles[0][1]
                    else:
                        nuevo_nodo = arcos_posibles[0][0]

                    nueva_ruta = cola_ruta[0:i+1]
                    nueva_ruta.append(nuevo_nodo)
                    return arcos_posibles[0], nueva_ruta
            return None

        while True:

            arco_seleccionado = criterionNode(criteria)

            if not arco_seleccionado:
                if not remainingArcs:
                    # Go to the depot
                    back_to_base()
                    return rute, remainingArcs
                # Calcular arcos que puedo atender
                nodos_atendibles = [(k, l) for k, l in remainingArcs.keys() if
                                    (rute._capacity - remainingArcs[(k, l)] >= 0)]
                # print(rute._capacity, nodos_atendibles)

                if not nodos_atendibles:
                    back_to_base()
                    return rute, remainingArcs
                if ENDING_STRATEGY == 0:
                    paths_and_distances = [self.shortestPathtoArc(rute.current_node(), (k, l), withdistance=True) for
                                           k, l in nodos_atendibles]

                    distances = [k for k, l in paths_and_distances]
                    index_arco_seleccionado = distances.index(min(distances))

                    rute.add_node(paths_and_distances[index_arco_seleccionado][1][1:])    #nueva ruta
                    rute._arcos_cubiertos.append(nodos_atendibles[index_arco_seleccionado]) #arco cubierto
                    remainingArcs.pop(nodos_atendibles[index_arco_seleccionado])            #arco cubierto
                    rute.reduce_capacity(self.get_demand(nodos_atendibles[index_arco_seleccionado][0],
                                                         nodos_atendibles[index_arco_seleccionado][1]))
                if ENDING_STRATEGY == 1:
                    nodos_adjacentes = []
                    for arco in nodos_atendibles:
                        for nodo in arco:
                            if nodo not in nodos_adjacentes:
                                nodos_adjacentes.append(nodo)
                    distancias_to_nodos = [self.getDistance(rute.current_node(), nodo) for
                                           nodo in nodos_adjacentes]
                    nodosel = nodos_adjacentes[distancias_to_nodos.index(min(distancias_to_nodos))]

                    rute.add_node(self.shortestPath(rute.current_node(), nodosel)[1:])  # nueva ruta

                if ENDING_STRATEGY == 2:

                    indexSel = max(range(len(nodos_atendibles)), key=lambda i: self.get_demand(nodos_atendibles[i][0],nodos_atendibles[i][1])       )

                    finCamino = self.shortestPathtoArc(rute.current_node(), nodos_atendibles[indexSel], withdistance=True)


                    ruta_alterna = verificador_ruta(finCamino[1])
                    if ruta_alterna is not None:
                        nodo_cubierto = ruta_alterna[0]
                        nueva_ruta = ruta_alterna[1]
                        rute.add_node(nueva_ruta[1:])  # nueva ruta
                        rute._arcos_cubiertos.append(nodo_cubierto)  # arco cubierto
                        remainingArcs.pop(nodo_cubierto)  # arco cubierto
                        rute.reduce_capacity(self.get_demand(nodo_cubierto[0],
                                                 nodo_cubierto[1]))
                    else:
                        rute.add_node(finCamino[1][1:])    #nueva ruta
                        rute._arcos_cubiertos.append(nodos_atendibles[indexSel]) #arco cubierto
                        remainingArcs.pop(nodos_atendibles[indexSel])            #arco cubierto
                        rute.reduce_capacity(self.get_demand(nodos_atendibles[indexSel][0],
                                                             nodos_atendibles[indexSel][1]))

                continue

            if arco_seleccionado[0] == rute.current_node():
                new_node = arco_seleccionado[1]
            else:
                new_node = arco_seleccionado[0]

            rute._arcos_cubiertos.append(arco_seleccionado)
            remainingArcs.pop(arco_seleccionado)
            rute.reduce_capacity(self.get_demand(rute.current_node(), new_node))

            rute.add_node(new_node)

        return rute, remainingArcs

    def pathScanning(self, random = False):


        k = 5
        if random:
            k=50


        no_factible = True
        while no_factible:
            rutas = [[] for i in range(k)]
            FO = [0] * k
            for i in range(k):  # i Metodo de regla
                remainingArcs = {i: self._graph[i][1] for i in self._graph.keys() if self._graph[i][1] > 0}

                for j in range(self._info["VEHICULOS"]):  # j Ruta creada
                    rutas[i].append(self.Ruta(self._info["CAPACIDAD"], self._info["DEPOSITO"]))
                    rutas[i][j], remainingArcs = self.selectorNode(i, rutas[i][j], remainingArcs, random)
                    if not remainingArcs:
                        break
                FO[i] = sum([k.funcion_objetivo(self._adjacency) for k in rutas[i]])
                if not remainingArcs:
                    pass
                else:
                    #Señala que el problema es infactible
                    FO[i] += float('Inf')
            if min(FO) == float('Inf'):
                if random and k>300:
                    out.write("No se encontro ningun set de rutas factibles\n")
                random = True
                k +=80
                if VERBOSE: out.write("Ningun set de rutas es factible con PS deterministico, cambiando modo a Aleatorizado k ="+str( k)+"\n")

            else:
                no_factible = False

        choosencriteria = FO.index(min(FO))
        if VERBOSE or SHOW_RESULTS:
            if ENDING_STRATEGY == 1:                modo = "Estrategia de Terminación Modificada"
            else:                modo = "Estrategia de Terminación Original"

            if random:
                out.write("Problem: "+ args[1].rstrip(".dat").lstrip("gdb/")+ "; Selección Aleatoria"+" " + modo + " FO:"+ str(FO[choosencriteria] )+"\n")
            else:
                out.write("Problem:" + args[1].rstrip(".dat").lstrip("gdb/") + "; Selección Determinista" +" " + modo + " FO:"+
                      str(FO[choosencriteria])+"\n")

        return rutas[choosencriteria], FO[choosencriteria]


def main(argv):
    global RANDOMIZED
    global out
    t1_start = perf_counter()
    file = str(argv[1])
    selection_nodes = RANDOMIZED
    if len(argv) >= 3:
        
        selection_nodes = bool(int(argv[2]))
        
    if len(argv) >= 4:
        global ENDING_STRATEGY
        ENDING_STRATEGY = int(argv[3])
    if len(argv) == 5:
        global VERBOSE
        VERBOSE = bool(int(argv[4]))

    out = open("output.txt", "a")
    

    grapho = Graph(file)
    bestRoutes, FO = grapho.pathScanning(selection_nodes)
    t1_stop = perf_counter()



    out.write("Elapsed time:"+ str(t1_stop- t1_start)+ "\n\n")
    print(FO, t1_stop- t1_start)

    if VERBOSE:
        for i in bestRoutes:


            out.write( "Arcos Cubiertos por "+str(i)+ ": "+ "Capacidad Utilizada: "+ str( sum([   grapho.get_demand(q,l) for q,l in i._arcos_cubiertos]))+"\n")
            for k,l in  i._arcos_cubiertos:
                out.write("("+str(k)+", "+str(l)+") ")
            out.write("\n")

    out.close()



if __name__ == "__main__":
    probarTodos = False

    if probarTodos:
        for i in range(1,24):
            args = [None,"gdb/gdb"+str(i) + ".dat"]

            main(args)

    else:
        if len(sys.argv) == 1:
            args = sys.argv
            args.append("gdb/gdb1.dat")
            main(args)
        else:
            args = sys.argv
            main(args)
