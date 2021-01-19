from ILS import *
from time import perf_counter

from os import listdir
from os.path import isfile, join
out = open("outputFINAL FINAL.txt", "a")
for i in range(2,5):
    dir = "./FK_"+str(i)+"/"
    files = [ f for f in listdir(dir) if not f.startswith('.') and isfile(join(dir, f))]
    out.write("Instancia,MAX_ITER,Lambda,max_pasos_sin_sol,max_pasos,FO,tiempo_Computacional \n")
    for file_path in files:
                    for i in range(20):
                        t1_init = perf_counter()
                        problem = MKnapsack(dir +file_path)
                        problem.initial_solution()
                        problem.ILS(max_iter=100, Lambda=0.01, max_pasos_sin_sol=50, max_pasos=35)
                        t1_stop = perf_counter()
                        out.write("FK" +str(i) +","+ ",".join([str(element) for element in file_path.split(sep="_")]) +","+ str( problem.fo)+","+ str(t1_stop - t1_init) )
                        out.write("\n")
                        del problem

