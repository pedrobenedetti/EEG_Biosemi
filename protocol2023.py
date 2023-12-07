#UPDATED 28/11/2023
#%% Import libraries
import pandas as pd
import math
import logging
import datetime
import sys
from pygame.locals import *
import pygame

#%% Set Path
# path = "C:/Users/pedro/Documents/Doctorado/protocol2023/"
# path = "D:/PROGRAMASYCARPETASESCRITORIO/Prueba_Pedro/protocol2023"
path = "D:\Pedro_Benedetti"

#%% Initiate Logger file
logging.basicConfig(filename="logger_protocol2023.txt", 
                    level=logging.DEBUG)
time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
mess0 = "\n Welcome to 2023 protocol"
logging.debug(mess0)
mess = (time_txt + ": Initializing protocol 2023...")
logging.debug(mess)


#%% Imports script where MATLAB fuctions are defined. MATLAB engine 
# will be started.
# https://github.com/pedrobenedetti/EEG_Biosemi/blob/aec354445dbbd8bd02cfd0500223e21c7e6a9995/matlab_parallel_com.py
try:
    from impparallel import *
except:
    # throws an exception and message if some error ocurred.
    print("Can't import 'impparallel'")
    time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess = (time_txt + ": Can't import 'matlab_parallel_com'")
    logging.error(mess)


#%% Protocol initiation
pygame.init() 
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#window = pygame.display.set_mode([500,500],RESIZABLE)
window.fill((0, 0, 0))
X, Y = window.get_size()
print(str(X),str(Y))
pygame.display.update()

#%%Variables initiation
port = 0xCFE8

page = 1
line_size = int(Y/20)
title_font = pygame.font.Font(None, line_size*2)  # Title font
body_font = pygame.font.Font(None, int(line_size*0.9))  # Body text font
input_font = pygame.font.Font(None, line_size)  # Input text font
time_font = pygame.font.Font(None, int(line_size*2.5))  # Time counter font
pink = (234, 64, 142)
purple = (169, 144, 210)
current_use = 1
use = ""
uses_array = []
uses_array.append("")
N_uses = 1
name = ""
age = ""
hand = ""
current_data = 1
clip = pygame.image.load(path + "/clip.png")
debug = 0
# Sound available on https://drive.google.com/file/d/1ZEsz7WcAmguzk7TIWu652IBkieHrBXdS/view?usp=share_link
#%% Cycle
time_start = datetime.datetime.now()
time_start_epoch = datetime.datetime.now()
while True:
    window.fill((0, 0, 0))
    time_now = datetime.datetime.now()
    if (time_now-time_start_epoch).total_seconds() > 5:
        send_mark_biosemi(page*10, port,debug)
        time_start_epoch = datetime.datetime.now()
#%% Page Switcher
    if page == 1: #DATOS PERSONALES
        title = title_font.render("INGRESA TUS DATOS", True, 
                                        pink)
        window.blit(title, (X/2-title.get_width()/2, line_size*3))
        if current_data == 1:
            text0 = input_font.render("Nombre:", True, 
                                        purple)
            text1 = input_font.render(name, True, 
                                         purple)
        else:
            text0 = body_font.render("Nombre:", True, 
                                        purple)
            text1 = body_font.render(name, True, 
                                         purple)
        window.blit(text0, (line_size, line_size*6))
        window.blit(text1, (text0.get_width()+line_size, line_size*6-int(0.05*line_size)))
        
        if current_data == 2:
            text2 = input_font.render("Edad: ", True, 
                                        purple)
            text3 = input_font.render(age, True, 
                                            purple)
        else:
            text2 = body_font.render("Edad: ", True, 
                                        purple)
            text3 = body_font.render(age, True, 
                                            purple)
        window.blit(text2, (line_size, line_size*7))
        window.blit(text3, (text2.get_width()+line_size, line_size*7-int(0.05*line_size)))
        
        if current_data == 3:
            text4 = input_font.render("Mano habil: ", True, 
                                        purple)
            text5 = input_font.render(hand, True, 
                                            purple)
        else:
            text4 = body_font.render("Mano habil: ", True, 
                                        purple)
            text5 = body_font.render(hand, True, 
                                            purple)
        window.blit(text4, (line_size, line_size*8))
        window.blit(text5, (text4.get_width()+line_size, line_size*8-int(0.05*line_size)))
        
        data_text = body_font.render("Usa las flechas ARRIBA y ABAJO para desplazarte entre los campos.", True, 
                                        purple)
        window.blit(data_text, (X/2-data_text.get_width()/2, line_size*17))
        next_text = body_font.render("Presioná 'Enter' para avanzar.", True, 
                                        purple)
        window.blit(next_text, (X/2-next_text.get_width()/2, line_size*18))   
    if page == 2: #INSTRUCCIONES GENERALES
        title = title_font.render("INSTRUCCIONES GENERALES", True, 
                                        pink)
        window.blit(title, (X/2-title.get_width()/2, line_size*3))
        text0 = body_font.render("A continuación, vas a realizar una serie de tareas que son parte de un estudio de neurociencias.", True, 
                                        purple)
        window.blit(text0, (line_size, line_size*6))
        text1 = body_font.render("Te pedimos que leas atentamente las instrucciones de cada una. Si tenés alguna duda o inconveniente ", True, 
                                        purple)
        window.blit(text1, (line_size, line_size*7))
        text2 = body_font.render("podés llamar a los investigadores ANTES de que comience la tarea en cuestión.", True, 
                                        purple)
        window.blit(text2, (line_size, line_size*8))
        text3 = body_font.render("No te rasques ni toques la cabeza. Una vez comenzada la tarea intenta moverte LO MENOS POSIBLE. ", True, 
                                        purple)
        window.blit(text3, (line_size, line_size*10))
        text4 = body_font.render("En caso de que tengas que escribir en la computadora, acomodate para hacerlo antes de comenzar. ", True, 
                                        purple)
        window.blit(text4, (line_size, line_size*11))
        text5 = body_font.render("Si tenés que escribir en papel, lo mismo: agarrá la lapicera/lapiz y acomoda el papel en frente tuyo.", True, 
                                        purple)
        window.blit(text5, (line_size, line_size*12))
        next_text = body_font.render("Presioná 'Enter' para avanzar.", True, 
                                        purple)
        window.blit(next_text, (X/2-next_text.get_width()/2, line_size*18))
    if page == 3: #INSTRUCCIONES RESTING
        title = title_font.render("INSTRUCCIONES TAREA 1", True, 
                                        pink)
        window.blit(title, (X/2-title.get_width()/2, line_size*3))
        text0 = body_font.render("En primer lugar, te vamos a pedir que te mantengas quieto/a durante 1 minuto mirando la cruz que vas a ver", True, 
                                        purple)
        window.blit(text0, (line_size, line_size*6))
        text1 = body_font.render("en el centro de la pantalla. Acomodate ahora, durante el minuto vas a tener que permanecer quieto/a. ", True, 
                                        purple)
        window.blit(text1, (line_size, line_size*7))
        text2 = body_font.render("Una vez trascurrido el minuto aparecerán las próximas indicaciones.", True, 
                                        purple)
        window.blit(text2, (line_size, line_size*8))
        next_text = body_font.render("Cuando estés listo/a presioná 'Enter' para comenzar.", True, 
                                        purple)
        window.blit(next_text, (X/2-next_text.get_width()/2, line_size*18))
    if page == 4: #RESTING
        title = title_font.render("+", True, 
                                        pink)
        window.blit(title, (X/2-title.get_width()/2, Y/2-title.get_height()))
        
        if (time_now-time_start).total_seconds() > 1*60:
            page = page + 1       
            send_mark_biosemi(page*10, port,debug)
            print("Pagina " + str(page))
            time_start = datetime.datetime.now()
            time_start_epoch = datetime.datetime.now()
    if page == 5: #INSTRUCCIONES REY
        title = title_font.render("INSTRUCCIONES TAREA 2", True, 
                                        pink)
        window.blit(title, (X/2-title.get_width()/2, line_size*3))
        text0 = body_font.render("Ahora tenés que dibujar de memoria la misma figura que hace dos días. ", True, 
                                        purple)
        window.blit(text0, (line_size, line_size*6))
        text1 = body_font.render("Vas a tener un minuto en el cual vas a tener que intentar recordarla, pero sin hacer nada.", True, 
                                        purple)
        window.blit(text1, (line_size, line_size*7))
        text2 = body_font.render("Durante ese minuto mirá fija a la cruz del centro de la pantalla.", True, 
                                        purple)
        window.blit(text2, (line_size, line_size*8))
        text3 = body_font.render("Pasado el minuto, vas a tener otros 3 minutos para dibujar la figura.", True, 
                                        purple)
        window.blit(text3, (line_size, line_size*10))
        text4 = body_font.render("Andá acomodándote y prepará adelante tuyo la hoja y la lapicera/lápiz", True, 
                                        purple)
        window.blit(text4, (line_size, line_size*11))
        
        next_text = body_font.render("Cuando estés listo/a presioná 'Enter' para comenzar.", True, 
                                        purple)
        window.blit(next_text, (X/2-next_text.get_width()/2, line_size*18))
    if page == 6: #REY PENSANDO
        title = title_font.render("+", True, 
                                        pink)
        window.blit(title, (X/2-title.get_width()/2, Y/2-title.get_height()))   
        if (time_now-time_start).total_seconds() > 1*60:
            page = page + 1 
            send_mark_biosemi(page*10, port,debug)
            print("Pagina " + str(page))
            time_start = datetime.datetime.now()
            time_start_epoch = datetime.datetime.now()
    if page == 7: #REY HACIENDO
        text0 = body_font.render("Ahora sí, dibujá la figura en la hoja que tenés adelante tuyo.", True, 
                                        purple)
        window.blit(text0, (X/2-text0.get_width()/2, line_size*6))
        text1 = body_font.render("Tenés 3 minutos. Si terminás antes presioná 'Enter'.", True, 
                                        purple)
        window.blit(text1, (X/2-text1.get_width()/2, line_size*7))
        if (time_now-time_start).total_seconds() > 3*60:
            page = page + 1
            print((time_now-time_start).total_seconds())
            send_mark_biosemi(page*10, port,debug)
            print("Pagina " + str(page))
            time_start = datetime.datetime.now()
            time_start_epoch = datetime.datetime.now()
    if page == 8: #INSTRUCCIONES 1 AUT
        title = title_font.render("INSTRUCCIONES TAREA 3", True, 
                                        pink)
        window.blit(title, (X/2-title.get_width()/2, line_size*3))
        text0 = body_font.render("El objetivo de esta tarea es escribir todos los usos alternativos que se te ocurran para un objeto. Después de iniciar, ", True, 
                                        purple)
        window.blit(text0, (line_size, line_size*6))
        text1 = body_font.render("escribí tus propuestas y presioná 'Enter' al terminar cada una. Usá tu imaginación para generar tus propuestas.", True, 
                                        purple)
        window.blit(text1, (line_size, line_size*7))
        text2 = body_font.render("No hay límites. Tu única limitación es el tiempo, vas a disponer de 1 minuto para pensar y 4 para escribirlos.", True, 
                                        purple)
        window.blit(text2, (line_size, line_size*8))
        
        text3 = body_font.render("Te damos un ejemplo: ¿Qué usos le darías a un papel de diario? Una respuesta podría ser 'Hacer un avión de papel'.", True, 
                                        purple)
        window.blit(text3, (line_size, line_size*10))
        
        
        text5 = body_font.render("Al comenzar te diremos cuál es el objeto en cuestión. Durante el primer minuto mirá fijo a la cruz en la pantalla.", True, 
                                        purple)
        window.blit(text5, (line_size, line_size*13))
        text6 = body_font.render("Luego, escribí todos los que se te ocurran en la computadora. Acomodate ahora como para hacerlo.", True, 
                                        purple)
        window.blit(text6, (line_size, line_size*14))
        
        next_text = body_font.render("Cuando estés listo/a presioná 'Enter' para comenzar.", True, 
                                        purple)
        window.blit(next_text, (X/2-next_text.get_width()/2, line_size*18))
    if page == 9: #INSTRUCCIONES 2 AUT
        text0 = body_font.render("Listo/a?", True, 
                                        purple)
        window.blit(text0, (X/2-text0.get_width()/2, line_size*4))
        text1 = body_font.render("Tu objeto es un clip para papel.", True, 
                                        purple)
        window.blit(text1, (X/2-text1.get_width()/2, line_size*5))
        next_text = body_font.render("Presioná 'Enter' para comenzar.", True, 
                                        purple)
        window.blit(next_text, (X/2-next_text.get_width()/2, line_size*18))
        window.blit(clip, (X/2-clip.get_width()/2, line_size*6))     
    if page == 10: #AUT PENSANDO
        title = title_font.render("+", True, 
                                        pink)
        window.blit(title, (X/2-title.get_width()/2, Y/2-title.get_height()))
        if (time_now-time_start).total_seconds() > 60:
            page = page + 1     
            send_mark_biosemi(page*10, port,debug)
            print("Pagina " + str(page))
            time_start = datetime.datetime.now()
            time_start_epoch = datetime.datetime.now()
    if page == 11: #AUT HACIENDO
        text0 = body_font.render("Ahora sí, escribí todos los usos que se te ocurran.", True, 
                                        purple)
        window.blit(text0, (line_size, line_size))
        for i in range(1,N_uses + 1):
            if i == current_use:
                number = input_font.render(str(i)+') ', True, 
                                            purple)
                use_text = input_font.render(uses_array[i-1], True, 
                                            purple)
                
                # print(uses_array)
                # print(i)
                # print(N_uses)
            else:
                number = body_font.render(str(i)+') ', True, 
                                            purple)
                use_text = body_font.render(uses_array[i-1], True, 
                                            purple)
            window.blit(number, (line_size, line_size * (i + 1)))
            window.blit(use_text, (number.get_width()+line_size, line_size * (i + 1)))
        if (time_now-time_start).total_seconds() > 4*60:
            page = page + 1
            send_mark_biosemi(page*10, port,debug)
            print("Pagina " + str(page))
            if current_use == N_uses:
                use = ""
                uses_array.append("")
                print(uses_array)
            time_start = datetime.datetime.now()
            time_start_epoch = datetime.datetime.now()                   
    if page == 12: #CHAU
        text0 = body_font.render("Listo, terminaste!", True, 
                                        purple)
        window.blit(text0, (X/2-text0.get_width()/2, line_size*4))
        text1 = body_font.render("Muchísimas gracias.", True, 
                                        purple)
        window.blit(text1, (X/2-text1.get_width()/2, line_size*5))
        next_text = body_font.render("Presioná 'Enter' para finalizar.", True, 
                                        purple)
        window.blit(next_text, (X/2-next_text.get_width()/2, line_size*18))
    pygame.display.update()
    
#%% Input Handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()                
            elif event.key == pygame.K_DOWN:
                if page == 1:
                    current_data = current_data + 1
                if page == 11:
                    if current_use != N_uses:
                        uses_array[current_use-1] = use
                        current_use = current_use + 1
                        use = uses_array[current_use - 1]
            elif event.key == pygame.K_UP:
                if page == 1:
                    current_data = current_data - 1
                if page == 11:
                    uses_array[current_use-1] = use
                    current_use = current_use - 1
                    use = uses_array[current_use - 1]
            elif event.key == pygame.K_BACKSPACE: 
                if page == 1:
                    name=name[0:-1]
                if page==11:
                    use = use[0:-1]
                    uses_array[current_use-1] = use
            elif event.key == pygame.K_RETURN:
                if page == 12:
                    pygame.quit()
                    sys.exit()   
                if page != 4 and page != 6 and page != 7 and page !=10 and page != 11:
                    page = page + 1
                    send_mark_biosemi(page*10, port ,debug)
                    print("Pagina " + str(page))
                    time_start= datetime.datetime.now()
                    time_start_epoch = datetime.datetime.now()                   
                if page == 11:
                    print(current_use)
                    print(N_uses)
                    if current_use == N_uses:
                        use = ""
                        uses_array.append("")
                        print(uses_array)
                        N_uses = N_uses + 1
                    else:
                        uses_array[current_use-1] = use
                        use =  uses_array[current_use]
                    current_use = current_use + 1
            else: #Si no es RETURN, BACKSPACE, UP, DOWN o SCAPE 
                if page==11:
                    use += event.unicode
                    uses_array[current_use-1] = use
                if page == 1:
                    if current_data == 1:
                        name += event.unicode
                    if current_data == 2:
                        age += event.unicode
                    if current_data == 3:
                        hand += event.unicode
