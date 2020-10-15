import copy
import sys
import numpy as np
from time import perf_counter
from math import comb

gen = np.random.default_rng()
# Tarea 2 Metaheuristicas
class problem:
    class ruta:
        def __init__(self, problema, posiciones=None):
            if posiciones is None:
                self._posterior = []
                self._anterior = []
                self._posiciones = []
                self._longitud = problema._nodos
            else:
                self._longitud = len(posiciones)
                self._posiciones = posiciones
                self._posterior = [None] * self._longitud
                self._anterior = [None] * self._longitud
                self.inicializar()

            self._problema = problema

        def MeineFO(self):
            FO = 0
            for desde, hacia in enumerate(self._posterior):
                FO +=self._problema.getDistance(desde,hacia)
            return FO


        def move3OPT(self, nodos):
            A,B,C = nodos[1], nodos[2], nodos[0]
            self._posterior[A], self._anterior[self._posterior[B]], self._posterior[C], self._anterior[self._posterior[A]], self._posterior[B], self._anterior[self._posterior[C]] = self._posterior[B], A, self._posterior[A], C, self._posterior[C], B

        def costoPosterior(self, nodo):
            return self._problema.getDistance(nodo, self._posterior[nodo])

        def costoAnterior(self, nodo):

            return self._problema.getDistance(self._anterior[nodo], nodo)

        def costoPromedioLlegar(self, nodo):
            costos = sum(self._problema._transposeDist[nodo][:nodo]) + sum(self._problema._transposeDist[nodo][nodo +1:])
            return costos /self._longitud


        def costoPromedioSalir(self, nodo):
            costos = sum(self._problema._distancias[nodo][:nodo]) + sum(
                self._problema._distancias[nodo][nodo + 1:])
            return costos / self._longitud

        def calculoswap(self, nodoA, nodoB):
            result = 0
            otronodo = nodoB
            for nodo in (nodoA, nodoB):
                result -= self._problema._distancias[self._anterior[nodo]][nodo]
                result -= self._problema._distancias[nodo][self._posterior[nodo]]
                result += self._problema._distancias[self._anterior[nodo]][otronodo]
                result += self._problema._distancias[otronodo][self._posterior[nodo]]
                otronodo = nodo
            return result

        def __copy__(self):
            new_instance = self._problema.ruta(self._problema)
            new_instance._posterior = copy.deepcopy(self._posterior)
            new_instance._anterior = copy.deepcopy(self._anterior)
            return new_instance

        def inicializar(self):
            for i, j in enumerate(self._posiciones):

                self._anterior[j] = self._posiciones[i - 1]
                if i == self._longitud - 1:
                    self._posterior[j] = self._posiciones[0]
                    break
                self._posterior[j] = self._posiciones[i + 1]

        def traduccion(self):
            self._posiciones = [0]
            for i in range(self._longitud - 1):
                self._posiciones.append(self._posterior[self._posiciones[-1]])

        def getPositions(self):
            self.traduccion()
            return self._posiciones

        def swap_nodes(self, nodeA, nodeB):
            antB = self._anterior[nodeB]
            antA = self._anterior[nodeA]
            postB = self._posterior[nodeB]
            postA = self._posterior[nodeA]
            self._anterior[nodeA], self._anterior[nodeB], self._posterior[nodeA], self._posterior[
                nodeB] = antB, antA, postB, postA
            self._posterior[antA], self._posterior[antB], self._anterior[postA], self._anterior[
                postB] = nodeB, nodeA, nodeB, nodeA

        def __str__(self):
            self.traduccion()
            return '{}({})'.format(self.__class__.__name__, (self._posiciones))

        def __repr__(self):
            self.traduccion()
            return '{}({})'.format(self.__class__.__name__, (self._posiciones))

    def __init__(self, file_name):
        self._info = {}
        self._distancias = []
        self._ruta_mas_cercana = []
        self._nearest_desde = []
        self._nearest_hasta = []
        self.getData(file_name)
        self._nodos = self._info["DIMENSION"]

        self._transposeDist = list(map(list, zip(*self._distancias)))


    def getData(self, file_name: str):
        handle = open(file_name)

        text, i, distances = handle.read().partition("EDGE_WEIGHT_SECTION")
        handle.close()
        info = {element[0]: element[1].strip() for element in [line.split(": ") for line in text.strip().split("\n")]}
        info["DIMENSION"] = int(info["DIMENSION"])
        self._distancias = np.fromstring(distances, sep='\n' , dtype= np.int16 , count=(info["DIMENSION"])*(info["DIMENSION"]))
        self._distancias = np.reshape(self._distancias, (info["DIMENSION"], info["DIMENSION"]))
        np.fill_diagonal(self._distancias, 9999)
        self._nearest_desde = np.argsort(self._distancias).tolist()

        self._nearest_hasta = np.argsort(self._distancias.T).tolist()
        #self._transposeDist = self._distancias.T.tolist()
        self._distancias = self._distancias.tolist()
        self._info = info




    def getDistance(self, origin, destination):
        return self._distancias[origin][destination]

    def nearestNeighbor(self):
        usedNodes = {0}
        self._ruta_mas_cercana.append(0)
        for i in range(self._nodos - 1):
            for j in self._nearest_desde[self._ruta_mas_cercana[-1]]:
                if j not in usedNodes:
                    self._ruta_mas_cercana.append(j)
                    usedNodes.add(j)
                    break
        return self.ruta(self, self._ruta_mas_cercana)

    def FO(self, Ruta):
        return sum([self._distancias[i][j] for i, j in enumerate(Ruta._posterior)])

    def swapAleatorioReloaded(self, ruta, MAX_ITER = None):
        if MAX_ITER is None:
            MAX_ITER = int((comb(ruta._longitud, 2)**(1/2))*120)
        for i in range(MAX_ITER):
            nodoA, nodeB = gen.choice(ruta._longitud, size=2, replace = False, shuffle=False)
            if ruta.calculoswap(nodoA, nodeB) < 0:
                ruta.swap_nodes(nodoA, nodeB)
        return ruta

    def TresOPT(self, ruta,  firstImprovement=False,MAX_ITER = None, itera = None):
        self._used = [False] * ruta._longitud
        if itera is None:
            itera = int(self._nodos ** (1 / 2) * 350)
        if MAX_ITER is None:
            MAX_ITER = 250

        for i in range(MAX_ITER):

            FOimprovement = 0

            combinaciones = random_combination3(np.array(ruta.getPositions()), sample =itera, number=3)
            for a,b,c in combinaciones:
                #Calculo 3OPT
                improvement = 0


                improvement -= (self._distancias[a][ruta._posterior[a]] +self._distancias[b][ruta._posterior[b]]  + self._distancias[c][ruta._posterior[c]]  )
                improvement += self._distancias[a][ruta._posterior[b]] +self._distancias[b][ruta._posterior[c]] + self._distancias[c][ruta._posterior[a]]



                if improvement < FOimprovement:
                    bestroute = (a,b,c)
                    FOimprovement = improvement
                    if firstImprovement:
                        break
            if (FOimprovement== 0):
                return ruta

            ruta.move3OPT(bestroute)

        return ruta

def random_combination3(posiciones, sample, number = 3):
    goodArray = gen.choice(len(posiciones), size=(sample, number))

    goodArray = np.delete(goodArray, np.where((
        goodArray[:, 0] == goodArray[:, 1]) | (goodArray[:, 1] == goodArray[:, 2]) | (goodArray[:, 0] == goodArray[:, 2])), axis=0)

    goodArray = np.sort(goodArray)
    posiciones = posiciones[goodArray]
    for i in posiciones:
        yield i.tolist()

def random_combination4(posiciones, sample, number = 3):
    pair = np.argpartition(gen.random((sample, len(posiciones))), number - 1, axis=-1)[:, :number]
    pair = np.sort(pair)
    for i in pair:
        yield posiciones[i]

probarTodos =  False
if __name__ == "__main__":
    #Parametros estandar
    file = "./MP-TESTDATA/rbg443.atsp.txt"
    heuristica = 1
    max_iter = None
    first_improve = 0
    num_combinations = None
    out = open("output.txt", "a")

    if len(sys.argv) > 1:
        file = sys.argv[1]
    if len(sys.argv) > 2:
        heuristica = int(sys.argv[2])
    if len(sys.argv) > 3:
        max_iter = int(sys.argv[3])
    if len(sys.argv) > 4:
        first_improve = int(sys.argv[4])
    if len(sys.argv) > 5:
        num_combinations = int(sys.argv[5])

    if file =="TODOS":

        out.write("Instancia \t FO SWAP \t Tiempo SWAP \t FO 3OPT BI \t Tiempo FO 3OPT BI \t FO 3OPT FI \t Tiempo 3OPT FI\n")
        from os import listdir
        from os.path import isfile, join

        dir = "./MP-TESTDATA/"
        files = [dir + f for f in listdir(dir) if not f.startswith('.') and isfile(join(dir, f))]

        for file in files:

            FOSWAP = []
            FO3OPTALL = []
            F03OPTFIRST = []
            timeSWAP = []
            time3OPTALL = []
            time3OPTFIRST = []
            ATSP = problem(file)
            ruta_constructiva = ATSP.nearestNeighbor()

            for i in range(10):
                t1_init = perf_counter()
                FOSWAP.append(ATSP.swapAleatorioReloaded(copy.copy(ruta_constructiva)).MeineFO())
                t1_stop = perf_counter()
                timeSWAP.append(t1_stop - t1_init)

                FO3OPTALL.append(ATSP.TresOPT(copy.copy(ruta_constructiva), firstImprovement=False).MeineFO())
                t1_init = perf_counter()
                time3OPTALL.append(t1_init - t1_stop)
                F03OPTFIRST.append(ATSP.TresOPT(copy.copy(ruta_constructiva), firstImprovement=True).MeineFO())
                t1_stop = perf_counter()
                time3OPTFIRST.append(t1_stop - t1_init)
            out.write(file[:-4] +"\t"+ str(sum(FOSWAP) / 10 )+ "\t"+str(sum(timeSWAP) / 10 )+"\t"+ str(sum(FO3OPTALL) / 10) +"\t"+ str(sum(time3OPTALL) / 10) +"\t"+
                      str( sum(F03OPTFIRST) / 10) + "\t"+ str(sum(time3OPTFIRST) / 10) +"\n")

    else:
        ATSP = problem(file)
        ruta_constructiva = ATSP.nearestNeighbor()

        out.write("Problema: " + ATSP._info["NAME"]+"\n")
        out.write("FO Ruta NN: " + str(ruta_constructiva.MeineFO())+"\n")

        if heuristica == 1:
            if first_improve == 0:
                text = "Best Improvement"
            else:
                text = "First Improvement"
            t1_init = perf_counter()
            ruta3OPT = ATSP.TresOPT(copy.copy(ruta_constructiva),   bool(first_improve), max_iter, num_combinations )
            print(file,". Función Obj: ", ruta3OPT.MeineFO(), ruta3OPT)
            t1_stop = perf_counter()
            out.write("FO Ruta 3OPT con " + text+ ": " +  str(ruta3OPT.MeineFO()) + "\tTiempo Computacional: " + str(t1_stop)  +"\n" )
        else:
            t1_init = perf_counter()
            rutaSwap = ATSP.swapAleatorioReloaded(copy.copy(ruta_constructiva), max_iter)
            print(file,". Función Obj: ", rutaSwap.MeineFO(), rutaSwap)
            t1_stop = perf_counter()
            out.write("FO Ruta Swap: " +  str(rutaSwap.MeineFO()) + "\tTiempo Computacional: " + str(t1_stop)  +"s\n")

    out.close()








