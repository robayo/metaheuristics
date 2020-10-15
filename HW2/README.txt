README
Tarea 2 Metaheuristicas
Nicolas Robayo Pardo
Todos los derechos reservados
201617123
11 Octubre 2020
¿Cómo ejecutar el programa?
Si hay una versión de Python3 >=3.8 instalada se puede usar el comando python HW1.py [args]
Si no hay una versión de Python, se adjunto un UNIX file para ser corrido en cualquier terminal de Linux o Mac con los parametros requeridos ubicado en dist/HW2/HW2. También se adjunto un .sh con los comandos para correr todas las instancias con todas las variantes. Este se encuentra en dist/HW2/scriptHW2.sh
Se debe correr, estando en la carpeta dist/HW1 en la terminal, como ./scriptHW2.sh

EL PROGRAMA SE DEBE EJECUTAR CON LOS SIGUIENTES PARAMETROS
a) Localización de la instancia a correr "MP-TESTDATA/rbg443.atsp.txt"

b) Heuristica de Búsqueda Local a utilizar
	0 para Swap, 1 para 3OPT
c) Número de máxima iteraciónes. Recomendado: 200 para 3OPT y 20000-40000 para swap
D) Si utilizar Best Improvement o First Improvement en la heuristics 3OPT (OPCIONAL)
	0 para Best Improvement
	1 para First Improvement
E) Número de combinaciones por iteracion (OPCIONAL)
	
Si se quieren correr todas las instancias como en el paper, escribir solo el parámetro "TODOS" como en $ python HW2.py TODOS

Los resultados se imprimirán en un archivo de texto output.txt en la carpeta de trabajo y las rutas en la consola.  