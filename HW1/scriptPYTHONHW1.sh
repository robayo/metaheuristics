echo "Modo deterministico tradicional"
python HW1.py "gdb/gdb1.dat" 0 2
python HW1.py "gdb/gdb2.dat" 0 2
python HW1.py "gdb/gdb3.dat" 0 2
python HW1.py "gdb/gdb4.dat" 0 2
python HW1.py "gdb/gdb5.dat" 0 2
python HW1.py "gdb/gdb6.dat" 0 2
python HW1.py "gdb/gdb7.dat" 0 2
echo "Modo deterministico modificado"
python HW1.py "gdb/gdb1.dat" 0 1
python HW1.py "gdb/gdb2.dat" 0 1
python HW1.py "gdb/gdb3.dat" 0 1
python HW1.py "gdb/gdb4.dat" 0 1
python HW1.py "gdb/gdb5.dat" 0 1
python HW1.py "gdb/gdb6.dat" 0 1
python HW1.py "gdb/gdb7.dat" 0 1
echo "Modo aleatorio tradicional"
python HW1.py "gdb/gdb1.dat" 1 2
python HW1.py "gdb/gdb2.dat" 1 2
python HW1.py "gdb/gdb3.dat" 1 2
python HW1.py "gdb/gdb4.dat" 1 2
python HW1.py "gdb/gdb5.dat" 1 2
python HW1.py "gdb/gdb6.dat" 1 2
python HW1.py "gdb/gdb7.dat" 1 2
echo "Modo aleatorio modificado"
python HW1.py "gdb/gdb1.dat" 1 1
python HW1.py "gdb/gdb2.dat" 1 1
python HW1.py "gdb/gdb3.dat" 1 1
python HW1.py "gdb/gdb4.dat" 1 1
python HW1.py "gdb/gdb5.dat" 1 1
python HW1.py "gdb/gdb6.dat" 1 1
python HW1.py "gdb/gdb7.dat" 0 1
echo "Revisar archivo output.txt para resultados completos.\n Para obtener las rutas añadir un 1 adicional en la linea de comandos"
python HW1.py "gdb/gdb1.dat" 1 1 1 