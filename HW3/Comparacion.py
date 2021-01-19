from HW3 import *
from time import perf_counter

filename = "comparacion.csv"
handle = open(filename, "a")

for tamañoTablero in reversed((8,10,25,50,100,200,300,400,500)):
                    for i in range(30):
                        t1_init = perf_counter()
                        chess_game = ChessBoard(tamañoTablero)
                        chess_game.simulated_annealing( InitialTemperature = 5, alpha=0.95, initialLenght = 1, increment_lenght=1,  MAXITER= 5000)
                        t1_stop = perf_counter()
                        handle.write(str(tamañoTablero)  +  ", "+ str(chess_game.fo) +", "+ str(t1_stop-t1_init) +"\n")
                        del chess_game
