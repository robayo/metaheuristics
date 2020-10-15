README
Tarea 1 Metaheuristicas
Nicolas Robayo Pardo
201617123
24 Septiembre 2020
¿Cómo ejecutar el programa?
Si hay una versión de Python3 instalada se puede usar el comando python HW1.py [args]
Si no hay una versión de Python, se adjunto un UNIX file para ser corrido en cualquier terminal de Linux o Mac con los parametros requeridos ubicado en dist/HW1/HW1. Tambien se adjunto un .sh con los comandos para correr todas las instancias con todas las variantes. Este se encuentra en dist/HW1/scriptHW1.sh
Se debe correr, estando en la carpeta dist/HW1 en la terminal, como ./scriptHW1.sh

EL PROGRAMA SE DEBE EJECUTAR CON LOS SIGUIENTES PARAMETROS
a) Localización de la instancia a correr "gdb/gdb1.dat"

b) Modo Aleatorizado o Deterministico
	0 para deterministico, 1 para aleatorizado
c) Modo de selección de nodos NO adyacentes tradicional o modificado
	1 para modificado
	2 para tradicional
d) OPCIONAL: Verbose: Si se desea imprimir las rutas generadas por el algoritmo.

Los resultados se imprimiran en un archivo de texto output.txt en la carpeta de trabajo. 