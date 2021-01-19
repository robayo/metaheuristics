README
Tarea 3 Metaheuristicas
Nicolas Robayo Pardo
Todos los derechos reservados
201617123
5 Noviembre 2020
¿Cómo ejecutar el programa?
Si hay una versión de Python3 >=3.8 instalada se puede usar el comando python HW3.py [args]
Si no hay una versión de Python, se adjunto un UNIX file para ser corrido en cualquier terminal de Linux o Mac con los parametros requeridos ubicado en dist/HW3/HW3. También se adjunto un .sh con los comandos para correr todas las instancias con todas las variantes. Este se encuentra en dist/HW3/scriptHW3.sh
Se debe correr, estando en la carpeta dist/HW3 en la terminal, como ./scriptHW3.sh

EL PROGRAMA SE DEBE EJECUTAR CON LOS SIGUIENTES PARAMETROS
a) Tamaño de tablero a resolver : 8
b) Temperatura Inicial: 100
c) Alpha para reducción geometrica de temperatura 0.9
d) Numero de iteraciones por paso de temperatura 1 
e) Maximo de Iteraciones sin resultado 10000
	
Si se quieren correr todas las instancias como en el paper, usar archivo  dist/HW3/scriptHW3.sh

Los resultados se imprimirán en un archivo de texto output.txt en la carpeta de trabajo y los dibujos de los tableros en el archivo "dibujos.txt"