from HW4 import *
from time import perf_counter
filename = "resultados.csv"
handle = open(filename, "a")
dir = "./P/"
files = [dir + f for f in listdir(dir) if not f.startswith('.') and isfile(join(dir, f)) and  f.endswith('.vrp')]
print(list(reversed(files)))
for i in range(10):
    for file in reversed(files):
        print(file)

        t1_init = perf_counter()
        instancia = CVRP(file)
        if instancia.info["DIMENSION"]<50:
            GENERACIONES = 1200
        else:
            GENERACIONES = 2000
        instancia.poblacion_inicial(poblacion=130)
        instancia.algoritmo_genetico(prob_cross=0.75, prob_mutacion=0.1, MAX_ITER=GENERACIONES, BCRC = False)
        t1_stop = perf_counter()
        handle.write(str(file) +", " +str(instancia.mejor_FO) + ", " +str(int(instancia.mejor_FO)/instancia.optimo - 1) +
                                                                         ", " + str(t1_stop - t1_init) + "\n")
handle.close()




