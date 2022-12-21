# UPDATED 21/12/2022
# AUT and REY protocol.

## PAGE ### TITLE ########## TIME MARK ##
## 0        PARTICIPANT CODE    -- ######
## 1        PART 1 TITLE        10 ######
## 2        INST. AUT           20 ######
## 3        THINK AUT           30 ######
## 4        AUT                 40 ######    
## 5        PART 2 TITLE        50 ######
## 6        INST REY            60 ######
## 7        THINK REY           70 ######
## 8        REY                 80 ######
## 9        THANKS              90 ######
## 10       RESTING             100 #####       
## 11       SAVING/END          110 #####
#########################################

path = "C:/Users/pbenedetti/Documents/Doctorado/Biosemi/Scripts"

####
##Import libraries
####
import pygame
from pygame.locals import *
import sys
import datetime
import logging
import math
import pandas as pd    

####
## Initiate Logger file
####
logging.basicConfig(filename = "logger_AUT_and_REY.txt", level = logging.DEBUG)
time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
mess0 = "\n Welcome to AUT and REY protocol"
logging.debug(mess0)
mess = (time_txt + ": Initializing protocol...")
logging.debug(mess)

####
## Imports script where MATLAB fuctions are defined. MATLAB engine will be started.
####
try:
    from matlab_parallel_com import *
except:
    # throws an exception and message if some error ocurred.
    print("Can't import 'matlab_parallel_com'")
    time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess = (time_txt + ": Can't import 'matlab_parallel_com'")
    logging.error(mess)

port = 'C020'

pygame.init() #Initiate pygame

####
# Send Mark indicating the protocol has started.
####



window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
window.fill((238, 238, 238))
X,Y = window.get_size()
pygame.display.update()

newsplane = pygame.image.load(path + '/newsplane.png') #Image available on https://drive.google.com/file/d/1khTMM9Fs5iIt-V4cTV5PTUFyKDczdU0g/view?usp=share_link
clip = pygame.image.load(path + "/clip.png") #Image available on https://drive.google.com/file/d/1RboI8fX5lwLC24OwUrFYIdizChEHX6wy/view?usp=share_link
soundObj = pygame.mixer.Sound(path + '/bell.wav') #Sound available on https://drive.google.com/file/d/1ZEsz7WcAmguzk7TIWu652IBkieHrBXdS/view?usp=share_link

pag_count=0 #Indicates in wich page of the protocol we are located
code = "" #Input text variable for participant code
input_rect = pygame.Rect(0,0,500,500) #Rectangle for input text
title_font = pygame.font.Font(None,60) #Title font
input_font = pygame.font.Font(None,32) #Body text font
time_font = pygame.font.Font(None, 100) #Time counter font
input_text = [] #List with uses saved
current_use = "" #Input text variable for currently wrinting use
N_uses = 0 #Number of uses saved on 'input_text'

output = [] #Output array
dt= "Date: " + str(datetime.datetime.now())
header = [dt]

while True: #permanently running
    if pag_count == 0: #PARTICIPANT CODE INPUT
        window.fill((238, 238, 238))
        text_surface = title_font.render("Codigo de participante: ", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2-100))
        text_surface2 = input_font.render(code, True, (74,64,103))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2,Y/2))
        text_surface3 = input_font.render("Presioná 'Enter' para avanzar.", True, (74,64,103))
        window.blit(text_surface3, (X/2-text_surface3.get_width()/2,Y-100))

    if pag_count == 1: #PART 1 TITLE (AUT)
        window.fill((238, 238, 238))
        text_surface = title_font.render("PARTE 1", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))

        text_surface8 = input_font.render("Presioná 'Enter' para avanzar.", True, (74,64,103))
        window.blit(text_surface8, (X/2-text_surface8.get_width()/2,Y-100))

    if pag_count == 2: #INSTRUCTIONS FOR AUT
        window.fill((238, 238, 238))

        text_surface = title_font.render("INSTRUCCIONES:", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, 50))
        
        text_surface2 = input_font.render("El objetivo es escribir todos los usos alternativos que se te ocurran para un objeto.", True, (74,64,103))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2,Y/2-150))
        
        text_surface3 = input_font.render("Después de iniciar, escribí tus propuestas y presioná 'Enter' al terminar cada una.", True, (74,64,103))
        window.blit(text_surface3, (X/2-text_surface3.get_width()/2,Y/2-125))
        
        text_surface4 = input_font.render("Usá tu imaginación para generar tus propuestas. No hay límites.", True, (74,64,103))
        window.blit(text_surface4, (X/2-text_surface4.get_width()/2,Y/2-75))
        
        text_surface5 = input_font.render("Tu única limitación es el tiempo, vas a disponer de 1 minuto para pensar y 4 para escribirlos.", True, (74,64,103))
        window.blit(text_surface5, (X/2-text_surface5.get_width()/2,Y/2-50))
        
        text_surface6 = input_font.render("Te damos un ejemplo: ¿Que usos le darías a un papel de diario?", True, (74,64,103))
        window.blit(text_surface6, (X/2-text_surface6.get_width()/2,Y/2+0))
        
        text_surface7 = input_font.render("Una respuesta podría ser 'Hacer un avión de papel'", True, (74,64,103))
        window.blit(text_surface7, (X/2-text_surface7.get_width()/2,Y/2+25))
        
        window.blit(newsplane, (X/2-newsplane.get_width()/2,Y/2+100))

    if pag_count == 3: #Thinking AUT
        window.fill((238, 238, 238))
        time_now = datetime.datetime.now()
        text_surface = title_font.render("Pensá: ¿Qué usos alternativos le darías a un clip?", True, (234, 64, 142))
        window.blit(text_surface,(X/2-text_surface.get_width()/2, 5))

        text_surface2 = time_font.render("+", True, (234, 64, 142))
        window.blit(text_surface2,(X/2-text_surface2.get_width()/2, Y/2))

        window.blit(clip, (X-clip.get_width(),Y/2-clip.get_height()/2))

        if (time_now - time_start).total_seconds() > 60:
            pag_count = pag_count + 1
            send_mark_biosemi(pag_count*10,port)
            time_start = datetime.datetime.now()
            started_AUT = 0


        text_surface3 = input_font.render("En breve vas a poder escribirlos.", True, (74,64,103))
        window.blit(text_surface3,(X/2-text_surface3.get_width()/2, Y-50))

    if pag_count == 4: #AUT
        window.fill((238, 238, 238))
        time_now = datetime.datetime.now()
        
        if started_AUT == 0:
            if (time_now-time_start).total_seconds()  < 1:
                text_surface = title_font.render("3", True, (234, 64, 142))
                window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))
                
            elif (time_now-time_start ).total_seconds() < 2:
                
                text_surface = title_font.render("2", True, (234, 64, 142))
                window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))
                
            elif (time_now - time_start).total_seconds() < 3:
                
                text_surface = title_font.render("1", True, (234, 64, 142))
                window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))
                soundObj.play()

            if (time_now - time_start).total_seconds() > 3:
                time_start = datetime.datetime.now() 
                soundObj.stop()
                started_AUT = 1
                send_mark_biosemi(pag_count*10 + 5,port)

        else:
            c=0
            pygame.draw.rect(window,(238,238,238), input_rect)
            text_surface = title_font.render("¿Qué usos alternativos le darías a un clip?", True, (234, 64, 142))
            window.blit(text_surface,(X/2-text_surface.get_width()/2, 5))
            if len(input_text) > 0:
                for x in input_text:
                    c=c+1
                    text_surface = input_font.render((str(c)+") "+x), True, (74,64,103))
                    window.blit(text_surface,(input_rect.x + 5, input_rect.y + c * 30+15))
                    input_rect.w = max(100,text_surface.get_width()+10)
                    input_rect.h = text_surface.get_height()*N_uses+10
            text_surface2 = input_font.render((str(N_uses+1)+") "+ current_use), True, (74,64,103))
            window.blit(text_surface2,(input_rect.x + 5, input_rect.y + (N_uses+1) * 30+15))

            segs = (time_now-time_start).total_seconds()
            mins = math.modf(3-(segs // 60))
            segs_rest = math.modf(60-(segs % 60))
            text_surface3 = time_font.render(str(int(mins[1]))+":"+str(int(segs_rest[1])), True, (234, 64, 142))
            window.blit(text_surface3,(X-clip.get_width()/2-text_surface3.get_width()/2,10))
            window.blit(clip, (X-clip.get_width(),Y/2-clip.get_height()/2))

            if (time_now-time_start).total_seconds()  > 4*60:
                soundObj.play()
                input_text.append(current_use)
                output.append(current_use)
                print(output)
                pag_count = pag_count + 1
                send_mark_biosemi(pag_count*10,port)
                
    
    if pag_count == 5: #TILE PART 2 (REY FIGURE TEST)
        window.fill((238, 238, 238))

        text_surface = input_font.render("Se acabó el tiempo. Pasamos a la siguiente parte:", True, (74,64,103))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, 50))

        text_surface2 = title_font.render("PARTE 2", True, (234, 64, 142))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2,Y/2))

        text_surface8 = input_font.render("Presioná 'Enter' para avanzar.", True, (74,64,103))
        window.blit(text_surface8, (X/2-text_surface8.get_width()/2,Y-100))
    
    if pag_count == 6: #INSTRUCTIONS REY FIGURE TEST
        window.fill((238, 238, 238))

        text_surface = title_font.render("INSTRUCCIONES:", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, 50))

        text_surface2 = input_font.render("Por último, tenés que dibujar de memoria la misma figura que hace dos días.", True, (74,64,103))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2,Y/2))

        text_surface3 = input_font.render("Tenés un tiempo de 1 minuto para pensar y 3 minutos para dibujar.", True, (74,64,103))
        window.blit(text_surface3, (X/2-text_surface3.get_width()/2,Y/2+50))

        text_surface4 = input_font.render("Presioná 'Enter' para comenzar.", True, (74,64,103))
        window.blit(text_surface4, (X/2-text_surface4.get_width()/2,Y/2+100))
    
    if pag_count == 7: #Thinking REY
        window.fill((238, 238, 238))
        time_now = datetime.datetime.now()
        text_surface = title_font.render("Recordá la figura que dibujaste hace dos días.", True, (234, 64, 142))
        window.blit(text_surface,(X/2-text_surface.get_width()/2, 5))

        text_surface2 = time_font.render("+", True, (234, 64, 142))
        window.blit(text_surface2,(X/2-text_surface2.get_width()/2, Y/2))

        text_surface3 = input_font.render("En breve vas a poder comenzar a dibujarla.", True, (74,64,103))
        window.blit(text_surface3,(X/2-text_surface3.get_width()/2, Y-50))

        if (time_now - time_start).total_seconds() > 60:
            pag_count = pag_count + 1
            time_start = datetime.datetime.now()
            send_mark_biosemi(pag_count*10,port)
            started_REY = 0

    if pag_count == 8: #REY FIGURE TEST TIME
        window.fill((238, 238, 238))
        time_now = datetime.datetime.now()

        if started_REY == 0:
            if (time_now-time_start).total_seconds()  < 1:
                text_surface = title_font.render("3", True, (234, 64, 142))
                window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))
                
            elif (time_now-time_start ).total_seconds() < 2:
                
                text_surface = title_font.render("2", True, (234, 64, 142))
                window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))
                
            elif (time_now - time_start).total_seconds() < 3:
                
                text_surface = title_font.render("1", True, (234, 64, 142))
                window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))
                soundObj.play()

            if (time_now - time_start).total_seconds() > 3:
                time_start = datetime.datetime.now() 
                soundObj.stop()
                started_REY = 1
                send_mark_biosemi(pag_count*10 + 5,port)

        else:
            segs = (time_now-time_start).total_seconds()
            mins = math.modf(2-(segs // 60))
            segs_rest = math.modf(60-(segs % 60))
            text_surface3 = time_font.render(str(int(mins[1]))+":"+str(int(segs_rest[1])), True, (234, 64, 142))
            window.blit(text_surface3,(X-150,10))

            if (time_now-time_start).total_seconds()  > 3*60:
                soundObj.play()
                pag_count = pag_count + 1
                send_mark_biosemi(pag_count*10,port)

    if pag_count == 9: #THANKS
        window.fill((238, 238, 238))
        text_surface = title_font.render("Muchas gracias por participar!", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))

        text_surface2 = title_font.render("Solo te pedimos que prestes atención durante", True, (234, 64, 142))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2, Y/2+text_surface2.get_height()))

        text_surface3 = title_font.render("un minuto a la cruz de la siguiente pantalla.", True, (234, 64, 142))
        window.blit(text_surface3, (X/2-text_surface3.get_width()/2, Y/2+text_surface2.get_height()*2))

        text_surface8 = input_font.render("Presioná 'Enter' para avanzar.", True, (74,64,103))
        window.blit(text_surface8, (X/2-text_surface8.get_width()/2,Y-100))

    if pag_count == 10: #Resting
        window.fill((238, 238, 238))
        text_surface = title_font.render("+", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))
        time_now = datetime.datetime.now()

        if (time_now-time_start).total_seconds()  > 60:
            pag_count = pag_count + 1
            send_mark_biosemi(pag_count*10,port)


    if pag_count == 11: #SAVING
        print(output)
        output = output
        filename = code + '_AUTandREY.csv'
        pygame.quit()
        data = pd.DataFrame(output, columns=header)
        data.to_csv(filename, index=False)
        sys.exit()

    pygame.display.update()




#############################################################################################
## Inputs handling ##########################################################################
#############################################################################################
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pag_count = pag_count # Nothing happens in this version
            elif event.key == pygame.K_ESCAPE:
                print(input_text)
                close_eng()
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_BACKSPACE: # If user needs to delete input text
                if pag_count == 4:
                    current_use = current_use[0:-1]
                if pag_count == 1:
                    code = code [0:-1]

            elif event.key == pygame.K_RETURN: # 'Enter' Button. Advance in pages and saves uses.
                
                if pag_count == 9:
                    pag_count = pag_count + 1
                    send_mark_biosemi(pag_count*10,port)
                    time_start = datetime.datetime.now() 

                if pag_count == 6:
                    pag_count = pag_count + 1
                    send_mark_biosemi(pag_count*10,port)
                    time_start = datetime.datetime.now() 

                if pag_count == 5:
                    pag_count = pag_count + 1
                    send_mark_biosemi(pag_count*10,port)

                if pag_count==4 and started_AUT == 1:
                    if len(current_use)>0:
                        input_text.append(current_use)
                        output.append(current_use)
                        current_use = ""
                        N_uses = N_uses + 1

                if pag_count == 2:
                    pag_count = pag_count + 1
                    time_start = datetime.datetime.now() 
                    send_mark_biosemi(pag_count*10,port)


                if pag_count == 1:
                    pag_count = pag_count + 1
                    send_mark_biosemi(pag_count*10,port)
    
                if pag_count == 0:
                    output.append("Participant: " + code)
                    pag_count = pag_count + 1
                    send_mark_biosemi(pag_count*10,port)
                
            else: #If button pressed is not 'Enter', 'Backspace' or Right arrow. Builds input text.
                if pag_count == 0:
                    code += event.unicode
                if pag_count == 4 and started_AUT == 1:
                    current_use += event.unicode
                

        if event.type == pygame.QUIT: #If user quits.
            logging.debug(str(output))
            logging.debug(mess)
            close_eng()
            pygame.quit()
            sys.exit()