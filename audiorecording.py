from impparallel import *
import datetime

port = 0xCFE8
debug = 1 #Dejar en 1 si se quiere probar en otra computadora, 0 para cuando se quiere hacer el experimento
resting = 1 #Dejar en 1 si es el resting, 0 si es la tarea 
escenario = 2 #4, 5 o 6

time_start = datetime.datetime.now()
count = 0
if resting == 1:
    mark = 50
else:
    mark = 100 + escenario * 10
send_mark_biosemi(mark,port,debug)

while True:
    time_now = datetime.datetime.now()

    if (time_now-time_start).total_seconds() > 5:
        send_mark_biosemi(mark,port,debug)
        time_start = datetime.datetime.now()
        if resting == 1:
            count = count + 1
            if count == 12:
                break
         
        
        
#Ctrl + C para cortar la tarea, el resting para solo
