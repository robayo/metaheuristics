README
Tarea 4 Metaheuristicas
Nicolas Robayo Pardo
Todos los derechos reservados
201617123
11 Diciembre 2020
¿Cómo ejecutar el programa?
Si hay una versión de Python3 >=3.8 instalada se puede usar el comando python HW4.py [args]
Si no hay una versión de Python, se adjunto un UNIX file para ser corrido en cualquier terminal de Linux o Mac con los parametros requeridos ubicado en dist/HW4/HW4. También se adjunto un .sh con los comandos para correr todas las instancias con todas las variantes. Este se encuentra en dist/HW4/scriptHW4.sh
Se debe correr, estando en la carpeta dist/HW4 en la terminal, como ./scriptHW4.sh

EL PROGRAMA SE DEBE EJECUTAR CON LOS SIGUIENTES PARAMETROS
a) Localización de la instancia a correr "./P/P-n55-k15.vrp"

b) Probbailidad de crossover [0.6,0.8]
c) Probabilidad de mutación [0.02,0.2]
D) MAX_ITER: Número de generacines [800,3000] Depende del tamaño del problema
E) Tipo de Crossover a utilizar: 1 para BCRC, 0 para partially map crossover
F) Tamaño de la población [800,1500]
	
Los resultados se imprimirán en un archivo de texto output.txt en la carpeta de trabajo.

La verdadera conclusion de este trabajo es que hay que dejar el Autosave prendido.