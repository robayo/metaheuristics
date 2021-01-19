from HW3 import *
from time import perf_counter

filename = "output.csv"
handle = open(filename, "w")
handle.write("Tamano Tablero, Tmax, Alpha, initialLenght,  FO, Tiempo\n")
for tamañoTablero in reversed((8, 25, 50, 75, 100, 200, 300, 500)):
    print(tamañoTablero)
    for Tmax in (5, 10, 50, 100):
        for alpha in (0.99,  0.95, 0.9, 0.85):
            for initialLenght in (1, 2, 5, 10, 15, 20):
                    for i in range(30):
                        t1_init = perf_counter()
                        chess_game = ChessBoard(tamañoTablero)
                        chess_game.simulated_annealing( InitialTemperature = Tmax, alpha=alpha, initialLenght = initialLenght, increment_lenght=1,  MAXITER= 500)
                        t1_stop = perf_counter()
                        handle.write(str(tamañoTablero) + ", " +str(Tmax) + ", " +str(alpha)+ ", "+ str(initialLenght)  +  ", "+ str(chess_game.fo) +", "+ str(t1_stop-t1_init) +"\n")
                        del chess_game
