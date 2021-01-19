from HW4 import *
from time import perf_counter

filename = "output.csv"
handle = open(filename, "w")
dir = "./P/"
files = [dir + f for f in listdir(dir) if not f.startswith('.') and isfile(join(dir, f)) and  f.endswith('.vrp')]
files = ["./P/" + i for i in ["P-n19-k2.vrp", "P-n23-k8.vrp", "P-n55-k8.vrp", "P-n76-k5.vrp"]]
for i in range(30):
    for file in files:
        for prob_cross in (0.65,0.7,0.75):
            for prob_mutacion in (0.05, 0.1):
                for MAX_ITER in (800,1200,1600,2000):
                    for BCRC in (True, False):
                        for poblacion in (70,100,130):
                            t1_init = perf_counter()
                            instancia = CVRP(file)
                            instancia.poblacion_inicial(poblacion=poblacion)
                            try:
                                instancia.algoritmo_genetico(prob_cross=prob_cross, prob_mutacion=prob_mutacion, MAX_ITER=MAX_ITER, BCRC = BCRC)
                            except:
                                continue
                            t1_stop = perf_counter()
                            handle.write(str(file) + ", " + str(prob_cross) + ", " + str(prob_mutacion) + ", " + str(
                                MAX_ITER) + ", " + str(BCRC) + ", " + str(poblacion) + ", " +str(instancia.mejor_FO) + ", " +str(instancia.mejor_FO/instancia.optimo - 1) +
                                                                                             ", " + str(t1_stop - t1_init) + "\n")
                            print(file)
                            print(instancia.mejor_FO)
                            print(instancia.optimo)

handle.close()




