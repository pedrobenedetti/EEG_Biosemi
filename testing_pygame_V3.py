#Updated 12/7/2022
import pygame
import sys
import time 
import logging
import datetime

logging.basicConfig(filename="logger_testingPyG.txt", level=logging.DEBUG)
time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
mess0="\n Welcome to probando pygame V3 protocol"
logging.debug(mess0)
mess=(time_txt + ": Initializing pygame V3 protocol...")
logging.debug(mess)

port='0xC020'

try:
    from matlab_parallel_com import *
except:
    print("Can't import 'matlab_parallel_com'")
    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess=(time_txt + ": Can't import 'matlab_parallel_com'")
    logging.error(mess)
    
#100 open, 200 close, 50 starts protocol, 20 next page, 10 closes protocol
pygame.init()
try:
    send_mark_biosemi(port,50)
except:
    print("Can't execute 'send_mark_biosemi' properly")
    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
    logging.error(mess)
    
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
clock = pygame.time.Clock()
X,Y=screen. get_size()
linea=50

dialogue_font = pygame.font.Font(None, linea)
dialogue = dialogue_font.render("Bienvenido al experimento.", True, (0,0,0))
dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))
dialogue1 = dialogue_font.render("", True, (0,0,0))
dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
dialogue2 = dialogue_font.render("Presione -> para continuar. Q para salir.", True, (0,0,0))
dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))

page=0
cuenta=3
cont_c=0
cont_a=0
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if page != 1:
                    page=page-1
            if event.key == pygame.K_RIGHT:
                page=page+1
                try:
                    send_mark_biosemi(port,20)
                except:
                    print("Can't execute 'send_mark_biosemi' properly")
                    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
                    logging.error(mess)
            if event.key==pygame.K_q:
                try:
                    send_mark_biosemi(port,10)
                except:
                    print("Can't execute 'send_mark_biosemi' properly")
                    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
                    logging.error(mess)
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            try:
                send_mark_biosemi(port,10)
            except:
                print("Can't execute 'send_mark_biosemi' properly")
                time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
                logging.error(mess)
            pygame.quit()
            sys.exit()
    
    if page==7:
        dialogue = dialogue_font.render("Terminaste",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))
        dialogue1 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
        dialogue2 = dialogue_font.render("Muchas gracias", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
    saltear=0
    
    
    if page==7:
        dialogue = dialogue_font.render("Listo!",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))
        dialogue1 = dialogue_font.render("Muchas gracias por tu tiempo!", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
        dialogue2 = dialogue_font.render("Presiona Q para salir.", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
    
    
    if page ==6:
        cont_a=cont_a+1
        if cont_a != 5:
            time.sleep(5)#abiertos
            soundObj.play()
            time.sleep(1) # wait and let the sound play for 1 second
            try:
                send_mark_biosemi(port,100)
            except:
                print("Can't execute 'send_mark_biosemi' properly")
                time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
                logging.error(mess)
        print("Opened", cont_a, "times")
        print(page)
        soundObj.stop()
        dialogue = dialogue_font.render("",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))
        dialogue1 = dialogue_font.render("Manten?? tus ojos cerrados.", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
        dialogue2 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
        if cont_a==5:
            page=7
        else: 
            page=5
        saltear=1

    
    if page==5 and saltear==0:
        time.sleep(5)#Cerrados
        cont_c=cont_c+1
        print("Closed", cont_c, "times")
        print(page)
        dialogue = dialogue_font.render("",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))

        dialogue1 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  

        dialogue2 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
        
        soundObj.play()
        time.sleep(1) # wait and let the sound play for 1 second
        soundObj.stop()

        soundObj.play()
        time.sleep(1) # wait and let the sound play for 1 second
        soundObj.stop()
        try:
            send_mark_biosemi(port,200)
        except:
            print("Can't execute 'send_mark_biosemi' properly")
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
            logging.error(mess)
        page=page+1

        dialogue = dialogue_font.render("Abr?? los ojos y mantenelos abiertos.",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))        
        dialogue1 = dialogue_font.render("Al escuchar un sonido volv?? cerrar los ojos.", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  
        dialogue2 = dialogue_font.render("Al escuchar un doble sonido abrilos.", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
                

    if page==4:
        soundObj = pygame.mixer.Sound('D:/Doctorado/Biosemi/Probando-pygame/tum.wav')
        soundObj.play()
        time.sleep(1) # wait and let the sound play for 1 second
        soundObj.stop()
        try:
            send_mark_biosemi(port,100)
        except:
            print("Can't execute 'send_mark_biosemi' properly")
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
            logging.error(mess)
        dialogue = dialogue_font.render("",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))

        dialogue1 = dialogue_font.render("Manten?? tus ojos cerrados.", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  

        dialogue2 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
        page=page+1
        

    if page==3:

        dialogue = dialogue_font.render("",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))

        dialogue1 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  

        dialogue2 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea)) 

        
        dialogue1 = dialogue_font.render(str(cuenta), True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
        time.sleep(1)
        
        if cuenta==0:
            page=page+1
            dialogue1 = dialogue_font.render("", True, (0,0,0))
            dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
        cuenta=cuenta-1


    if page==2:
        
        dialogue = dialogue_font.render("Est??s listo?",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))

        dialogue1 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  

        dialogue2 = dialogue_font.render("Presione -> para continuar.  Q para salir.", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea)) 
    

    if page==1:
            
            dialogue = dialogue_font.render("En breve comenzar?? una cuenta regresiva. Al llegar a cero",True, (0,0,0)) 
            dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))

            dialogue1 = dialogue_font.render("y escuchar un sonido deber??s cerrar los ojos.", True, (0,0,0))
            dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  

            dialogue2 = dialogue_font.render("Al escuchar un doble sonido deber??s abrirlos.", True, (0,0,0))
            dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea)) 


        
    screen.fill((255, 255, 255))
     
    screen.blit(dialogue, dialogue_rect)
    screen.blit(dialogue1, dialogue_rect1)
    screen.blit(dialogue2, dialogue_rect2)
     
    pygame.display.flip()
    clock.tick(60)
