        p1 = random.randrange(len(string_ruta_1))
        p2 = random.randrange(p1+1, len(string_ruta_1)+1)
        selectedp1 = string_ruta_1[p1:p2]
        selectedp2 = string_ruta_2[p1:p2]
        string_ruta_1[p1:p2], string_ruta_2[p1:p2] = string_ruta_2[p1:p2], string_ruta_1[p1:p2]
        #Repetidos
        repetidos = set(selectedp1).intersection(selectedp2)

        for repetido in repetidos:
            index1, index2 = selectedp1.index(repetido), selectedp2.index(repetido)
            pareja2, pareja1 = selectedp2[index1], selectedp1[index2]
            for posicion, nodo in enumerate(string_ruta_1):
                if not (posicion >= p1 and posicion < p2) and nodo == pareja1:
                    string_ruta_1[posicion] = pareja2
                    break
            for posicion, nodo in enumerate(string_ruta_2):
                if not (posicion >= p1 and posicion < p2) and nodo == pareja2:
                    string_ruta_2[posicion] = pareja1
                    break


        for posicion, nodo in enumerate(string_ruta_1):
            if not (posicion >= p1 and posicion < p2) and nodo in selectedp2 and nodo not in repetidos:
                index = string_ruta_1[p1:p2].index(nodo)
                string_ruta_1[posicion] = string_ruta_2[p1 + index]


        for posicion, nodo in enumerate(string_ruta_2):
            if not (posicion >= p1 and posicion < p2) and nodo in selectedp1 and nodo not in repetidos:
                index = string_ruta_2[p1:p2].index(nodo)
                string_ruta_2[posicion] = string_ruta_1[p1 + index]
