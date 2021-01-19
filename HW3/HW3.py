# Nicolas Robayo Pardo
# 24 Octubre  2020
# Tarea 3 Metaheuristicas
from math import exp
from random import sample, random, choice
from sys import argv
from time import perf_counter

class ChessBoard:
    def __init__(self, n, initSol=None):
        self.n = n
        if initSol is None:
            self.Sol = ["  "] * n
            self.create_solution(n)
        else:
            self.Sol = initSol

        self.diagonal_arriba = dict()
        self.diagonal_baja = dict()
        self.fo = None
        self.tablero = [""]*n
        self.iterador = list(diagonal_check(n))
        self.calcular_fo()

    def calcular_fo(self):
        self.fill_diagonals()
        fo = 0
        for diagonal in (self.diagonal_arriba, self.diagonal_baja):
            for key, set in diagonal.items():
                count = 0
                if len(set) > 1:
                    count += len(set) - 1
                fo += count / 1  # (self.n - abs(key - self.n)) #Normalización

        self.fo = fo

    def fill_diagonals(self):
        self.diagonal_arriba = dict()
        self.diagonal_baja = dict()

        for i, j in enumerate(self.Sol):
            self.diagonal_arriba.setdefault(i + j, set()).add(j)
            self.diagonal_baja.setdefault(self.n - 1 - i + j, set()).add(j)

    def create_solution(self, n):
        self.Sol = sample(range(n), k=n)

    def traduccion(self):
        # self.calcular_fo()
        for col, fila in enumerate(self.Sol):
            col, fila = int(col), int(fila)
            self.tablero[fila] = " □"*(col) + " ♕" + " □"*(self.n - col-1)

    def effective_swap(self):
        for diag in self.iterador:
            if diag in self.diagonal_arriba:
                if len(self.diagonal_arriba[diag]) > 1:

                    reina_remover = choice(
                        tuple(self.diagonal_arriba[diag]))  # fila = reina_remover , # column = diag-reina_remover
                    posibles_diagonales = self.diagonal_arriba.keys() - {diag}
                    if len(posibles_diagonales) == 0:
                        break
                    otra_diagonal = choice(tuple(posibles_diagonales))
                    otra_reina = choice(tuple(self.diagonal_arriba[otra_diagonal]))
                    # Posicion Nueva 1
                    # nuevaFila = reina_remover
                    nuevaColumna = otra_diagonal - otra_reina
                    # Posicion Nueva 2
                    # nuevaFila2 = otra_reina
                    nuevaColumna2 = diag - reina_remover
                    cambioFO = -1 - min(1, len(self.diagonal_arriba[otra_diagonal]) - 1)

                    cambioFO += min(1, len(self.diagonal_baja.get(self.n - 1 + otra_reina - nuevaColumna2, []))) + \
                                min(1, len(self.diagonal_baja.get(self.n - 1 + reina_remover - nuevaColumna, [])))

                    if self.n - 1 - diag + 2 * reina_remover == self.n - 1 - otra_diagonal + 2 * otra_reina and \
                            len(self.diagonal_baja.get(self.n - 1 - diag + 2 * reina_remover, [])) == 2:
                        cambioFO -= 1
                    else:
                        cambioFO += - min(1,
                                          len(self.diagonal_baja.get(self.n - 1 - diag + 2 * reina_remover, [])) - 1) - \
                                    min(1, len(
                                        self.diagonal_baja.get(self.n - 1 - otra_diagonal + 2 * otra_reina, [])) - 1)

                    if nuevaColumna + reina_remover == nuevaColumna2 + otra_reina and \
                            len(self.diagonal_arriba.get(nuevaColumna2 + otra_reina, [])) == 0:
                        cambioFO += 1
                    else:
                        cambioFO += min(1, len(self.diagonal_arriba.get(reina_remover + nuevaColumna, []))) + \
                                    min(1, len(self.diagonal_arriba.get(otra_reina + nuevaColumna2, [])))
                    return cambioFO, ((reina_remover, diag - reina_remover), (otra_reina, otra_diagonal - otra_reina))

        for diag in self.iterador:
            if diag in self.diagonal_baja:
                if len(self.diagonal_baja[diag]) > 1:
                    reina_remover = choice(tuple(self.diagonal_baja[diag]))  # fila = reina_remover , # column = diag-reina_remover
                    posibles_diagonales = self.diagonal_baja.keys() - {diag}
                    if len(posibles_diagonales) == 0:
                        break
                    otra_diagonal = choice(tuple(posibles_diagonales))
                    otra_reina = choice(tuple(self.diagonal_baja[otra_diagonal]))
                    # Posicion Nueva 1
                    nuevaFila = reina_remover
                    nuevaColumna = self.n - 1 - otra_diagonal + otra_reina

                    # Posicion Nueva 2
                    nuevaFila2 = otra_reina
                    nuevaColumna2 = self.n - 1 - diag + reina_remover

                    cambioFO = -1 - min(1, len(self.diagonal_baja[otra_diagonal]) - 1)

                    cambioFO += min(1, len(self.diagonal_arriba.get(nuevaFila2 + nuevaColumna2, []))) + \
                                min(1, len(self.diagonal_arriba.get(nuevaFila + nuevaColumna, [])))

                    if self.n - 1 - diag + 2 * reina_remover == self.n - 1 - otra_diagonal + 2 * otra_reina and \
                            len(self.diagonal_arriba.get(self.n - 1 - otra_diagonal + 2 * otra_reina, [])) == 2:
                        cambioFO -= 1
                    else:
                        cambioFO += - min(1, len(
                            self.diagonal_arriba.get(self.n - 1 - otra_diagonal + 2 * otra_reina, [])) - 1) - \
                                    min(1, len(self.diagonal_arriba.get(self.n - 1 - diag + 2 * reina_remover, [])) - 1)

                    if self.n - 1 - nuevaColumna + nuevaFila == self.n - 1 - nuevaColumna2 + nuevaFila2 and \
                            len(self.diagonal_baja.get(self.n - 1 - nuevaColumna + nuevaFila, [])) == 0:
                        cambioFO += 1
                    else:
                        cambioFO += min(1, len(self.diagonal_baja.get(self.n - 1 - nuevaColumna + nuevaFila, []))) + \
                                    min(1, len(self.diagonal_baja.get(self.n - 1 - nuevaColumna2 + nuevaFila2, [])))

                    return cambioFO, ((reina_remover, self.n - 1 + reina_remover - diag),
                                      (otra_reina, self.n - 1 + otra_reina - otra_diagonal))
        return None, None

    def realizarSwap(self, instrucciones):
        ((reina_remover, col_reinaremover), (otra_reina, col_otrareina)) = instrucciones
        # REMOVE
        ##diagonales reina original
        self.diagonal_baja[self.n - 1 + reina_remover - col_reinaremover].remove(reina_remover)
        self.diagonal_arriba[reina_remover + col_reinaremover].remove(reina_remover)
        ##diagonales_otra reina
        self.diagonal_baja[self.n - 1 + otra_reina - col_otrareina].remove(otra_reina)
        self.diagonal_arriba[otra_reina + col_otrareina].remove(otra_reina)

        # checks if diagonals are now empty
        if len(self.diagonal_baja[self.n - 1 + reina_remover - col_reinaremover]) == 0: self.diagonal_baja.pop(
            self.n - 1 + reina_remover - col_reinaremover)
        if len(self.diagonal_arriba[reina_remover + col_reinaremover]) == 0: self.diagonal_arriba.pop(
            reina_remover + col_reinaremover)
        if len(self.diagonal_baja.get(self.n - 1 + otra_reina - col_otrareina, "compartia la diagonal")) == 0:
            self.diagonal_baja.pop(self.n - 1 + otra_reina - col_otrareina)
        if len(self.diagonal_arriba[otra_reina + col_otrareina]) == 0:
            self.diagonal_arriba.pop(otra_reina + col_otrareina)

        # ADD
        ##diagonal nueva reina 1     # fila i = reina_remover, columna j = col_otrareina
        self.diagonal_baja.setdefault(self.n - 1 - col_otrareina + reina_remover, set()).add(reina_remover)
        self.diagonal_arriba.setdefault(col_otrareina + reina_remover, set()).add(reina_remover)
        ##diagonal nueva reina 2   # fila i =  otra_reina, columna j =  col_reinaremover
        self.diagonal_baja.setdefault(self.n - 1 - col_reinaremover + otra_reina, set()).add(otra_reina)
        self.diagonal_arriba.setdefault(col_reinaremover + otra_reina, set()).add(otra_reina)
        self.Sol[col_reinaremover] = otra_reina
        self.Sol[col_otrareina] = reina_remover

    def simulated_annealing(self, InitialTemperature = 2, alpha=0.95, initialLenght = 1, increment_lenght=1,  MAXITER= 1000):

        iter_no_result = 0
        temp = InitialTemperature
        lenght = initialLenght
        while iter_no_result < MAXITER:
            for tk in range(lenght):
                cambioFO, instrucciones_cambio = self.effective_swap()
                if cambioFO is None:
                    iter_no_result = MAXITER
                    break

                elif  cambioFO < 0 or (cambioFO >= 0 and exp(-cambioFO / temp) > random()):

                    self.realizarSwap(instrucciones_cambio)
                    self.fo += cambioFO
                    iter_no_result = 0
                else:
                    iter_no_result +=1

            temp = temp * alpha
            lenght = int(lenght * increment_lenght)

    def __str__(self):
        self.traduccion()
        return '\n'.join('{}'.format(item) for item in self.tablero) + "\n" + str(self.fo)

    def __repr__(self):
        self.traduccion()
        return '\n'.join('{}'.format(item) for item in self.tablero) + "\n" + str(self.fo)


def diagonal_check(n):
    yield n - 1
    for i in range(1, n - 1):
        yield n - 1 - i
        yield n - 1 + i
    yield n + i - 1


if __name__ == '__main__':
    tInit, alpha, L, MAXITER = 100,  0.9, 1, 1000
    if len(argv) > 1:
        n = int(argv[1])
        if len(argv) > 2:
            tInit = int(argv[2])
            if len(argv) > 3:
                alpha = float(argv[3])
                if len(argv) > 4:
                    L = int(argv[4])
                    if len(argv) > 5:
                        MAXITER = int(argv[5])


    else:
        n = 10

    handle = open("results.txt", "a")
    handle2 = open("dibujos.txt", "a")
    t1_init = perf_counter()
    chess_game = ChessBoard(n)
    chess_game.simulated_annealing(InitialTemperature = tInit, alpha=alpha, initialLenght = L, increment_lenght=1,  MAXITER= MAXITER)
    t1_stop = perf_counter()
    handle.write("Tablero de tamaño: " + str(n) +" | Función Objetivo: " + str(chess_game.fo)+"\n")
    handle.write("Solución: " + str(chess_game.Sol)+ " Tiempo Computacional (s): "+ str(t1_stop-t1_init) + "\n")
    handle2.write("Tablero n: " +str(n) + "\n" + str(chess_game) +"\n")
