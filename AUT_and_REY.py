# UPDATED 28/11/2022
# AUT and REY protocol.

import pygame
from pygame.locals import *
import sys
import datetime
import logging
import math
import pandas as pd    



logging.basicConfig(filename = "logger_AUT_and_REY.txt", level = logging.DEBUG)
time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
mess0 = "\n Welcome to AUT and REY protocol"
logging.debug(mess0)
mess = (time_txt + ": Initializing protocol...")
logging.debug(mess)

# try:
#     from matlab_parallel_com import *
#     # imports script where MATLAB fuctions are defined. MATLAB engine will be started.
# except:
#     # throws an exception and message if some error ocurred.
#     print("Can't import 'matlab_parallel_com'")
#     time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
#     mess = (time_txt + ": Can't import 'matlab_parallel_com'")
#     logging.error(mess)

#     port = 'C020'

pygame.init()
# # Initiate pygame
# try:
#     send_mark_biosemi(20, port)
#     # A mark (25) is sent to the EEG indicating that the code has started.
# except:
#     print("Can't execute 'send_mark_biosemi' properly")
#     time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
#     mess = (time_txt + ": Can't execute 'send_mark_biosemi' properly")
#     logging.error(mess)


window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)

newsplane = pygame.image.load('C:/Users/pbenedetti/Documents/Doctorado/Biosemi/Scripts/newsplane.png')
clip = pygame.image.load("C:/Users/pbenedetti/Documents/Doctorado/Biosemi/Scripts/clip.png")
window.fill((238, 238, 238))
# Fill the screen with white color

X,Y = window.get_size()
pygame.display.update()
pag_count=0
code = ""
input_rect = pygame.Rect(0,0,500,500)
active = False
title_font = pygame.font.Font(None,60)
input_font = pygame.font.Font(None,32)
time_font = pygame.font.Font(None, 100)
input_text = []
current_use = ""
N_uses = 0
soundObj = pygame.mixer.Sound('C:/Users/pbenedetti/Documents/Doctorado/Biosemi/Scripts/010762485_prev_1.wav')
output = []
dt= "Date: " + str(datetime.datetime.now())
header = [dt]
print(output)

while True:
    if pag_count == 0:
        window.fill((238, 238, 238))
        text_surface = title_font.render("Codigo de participante: ", True, (234, 64, 142))
        text_surface2 = input_font.render(code, True, (74,64,103))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2-100))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2,Y/2))

    if pag_count == 1:
        window.fill((238, 238, 238))
        text_surface = title_font.render("PARTE 1", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))

    if pag_count == 2:
        window.fill((238, 238, 238))
        text_surface = title_font.render("INSTRUCCIONES:", True, (234, 64, 142))
        text_surface2 = input_font.render("El objetivo es escribir todos los usos alternativos que se te ocurran para un objeto.", True, (74,64,103))
        text_surface3 = input_font.render("Después de iniciar, escribí tus propuestas y presioná 'Enter' al terminar cada una.", True, (74,64,103))
        text_surface4 = input_font.render("Usá tu imaginación para generar tus propuestas. No hay límites.", True, (74,64,103))
        text_surface5 = input_font.render("Tu única limitación es el tiempo, vas a disponer de 5 minutos.", True, (74,64,103))
        text_surface6 = input_font.render("Te damos un ejemplo: ¿Que usos le darías a un papel de diario?", True, (74,64,103))
        text_surface7 = input_font.render("Una respuesta podría ser 'Hacer un avión de papel'", True, (74,64,103))

        window.blit(text_surface, (X/2-text_surface.get_width()/2, 50))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2,Y/2-150))
        window.blit(text_surface3, (X/2-text_surface3.get_width()/2,Y/2-125))
        window.blit(text_surface4, (X/2-text_surface4.get_width()/2,Y/2-75))
        window.blit(text_surface5, (X/2-text_surface5.get_width()/2,Y/2-50))
        window.blit(text_surface6, (X/2-text_surface6.get_width()/2,Y/2+0))
        window.blit(text_surface7, (X/2-text_surface7.get_width()/2,Y/2+25))
        window.blit(newsplane, (X/2-newsplane.get_width()/2,Y/2+100))
        

    if pag_count == 3:
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
            #print(N_uses)
            text_surface2 = input_font.render((str(N_uses+1)+") "+ current_use), True, (74,64,103))
            window.blit(text_surface2,(input_rect.x + 5, input_rect.y + (N_uses+1) * 30+15))

            segs = (time_now-time_start).total_seconds()
            mins = math.modf(4-(segs // 60))
            segs_rest = math.modf(60-(segs % 60))
            text_surface3 = time_font.render(str(int(mins[1]))+":"+str(int(segs_rest[1])), True, (234, 64, 142))
            window.blit(text_surface3,(X-clip.get_width()/2-text_surface3.get_width()/2,10))
            window.blit(clip, (X-clip.get_width(),Y/2-clip.get_height()/2))
            if (time_now-time_start).total_seconds()  > 5*60:
                soundObj.play()
                input_text.append(current_use)
                output.append(current_use)
                print(output)

                pag_count = pag_count + 1
                
    
    if pag_count == 4:
        window.fill((238, 238, 238))
        text_surface = input_font.render("Se acabó el tiempo. Pasamos a la siguiente parte:", True, (74,64,103))
        text_surface2 = title_font.render("PARTE 2", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, 50))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2,Y/2))

    if pag_count == 5:
        window.fill((238, 238, 238))
        text_surface = title_font.render("INSTRUCCIONES:", True, (234, 64, 142))
        text_surface2 = input_font.render("Por último, tenés que dibujar la misma figura que hace dos días.", True, (74,64,103))
        text_surface3 = input_font.render("Tenés un tiempo total de 3 minutos para hacerlo. Presioná 'Enter' para comenzar.", True, (74,64,103))

        window.blit(text_surface, (X/2-text_surface.get_width()/2, 50))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2,Y/2))
        window.blit(text_surface3, (X/2-text_surface3.get_width()/2,Y/2+50))

    if pag_count == 6:
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

        else:
            segs = (time_now-time_start).total_seconds()
            mins = math.modf(2-(segs // 60))
            segs_rest = math.modf(60-(segs % 60))
            text_surface3 = time_font.render(str(int(mins[1]))+":"+str(int(segs_rest[1])), True, (234, 64, 142))
            window.blit(text_surface3,(X-150,10))

            if (time_now-time_start).total_seconds()  > 3*60:
                soundObj.play()
                pag_count = pag_count + 1

    if pag_count == 7:
        window.fill((238, 238, 238))
        text_surface = title_font.render("MUCHAS GRACIAS POR PARTICIPAR!", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2))
    
    if pag_count == 8:
        print(output)
        output = output
        filename = code + '_AUTandREY.csv'
        pygame.quit()
        data = pd.DataFrame(output, columns=header)
        data.to_csv(filename, index=False)
        sys.exit()



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else: 
                active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pag_count = pag_count + 1
            elif event.key == pygame.K_ESCAPE:
                print(input_text)
                # the user can quit the protocol by pressing Q key
                # try:
                # # one last mark is sent indicating that the protocol is over
                #     send_mark_biosemi(250, port)
                #     time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                #     mess = (time_txt + ": Ending protocol..."+"\n")
                #     logging.debug(mess)
                # except:
                #     print("Can't execute 'send_mark_biosemi' properly")
                #     time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                #     mess = (time_txt + ": Can't execute 'send_mark_biosemi' properly")
                #     logging.error(mess)
                # close_eng()
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_BACKSPACE:
                if pag_count==3:
                    current_use = current_use[0:-1]

            elif event.key == pygame.K_RETURN:
                if pag_count == 7:
                    pag_count = pag_count + 1

                if pag_count == 5:
                    pag_count = pag_count + 1
                    time_start = datetime.datetime.now() 
                    started_REY = 0

                if pag_count == 4:
                    pag_count = pag_count + 1
                
                if pag_count==3 and started_AUT == 1:
                    if len(current_use)>0:
                        input_text.append(current_use)
                        output.append(current_use)
                        print(output)

                        current_use = ""
                        N_uses = N_uses + 1

                if pag_count == 2:
                    pag_count = pag_count + 1
                    started_AUT = 0
                    time_start = datetime.datetime.now() 

                if pag_count == 1:
                    pag_count = pag_count + 1
    
                if pag_count == 0:
                    output.append("Participant: " + code)
                    print(output)

                    pag_count = pag_count + 1
                



            else:
                if pag_count == 0:
                    code += event.unicode
                if pag_count == 3 and started_AUT == 1:
                    current_use += event.unicode
                

        if event.type == pygame.QUIT:
            # try:
            #     # one last mark is sent indicating that the protocol is over
            #     send_mark_biosemi(250, port)
            #     time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            #     mess = (time_txt + ": Ending protocol..."+"\n")
            # except:
            #     print("Can't execute 'send_mark_biosemi' properly")
            #     time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            #     mess = (time_txt + ": Can't execute 'send_mark_biosemi' properly")
            #     logging.error(mess)
            # logging.debug(mess)
            #close_eng()
            pygame.quit()
            sys.exit()