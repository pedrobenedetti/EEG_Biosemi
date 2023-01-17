# UPDATED 

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
#path = "D:/PROGRAMASYCARPETASESCRITORIO/Prueba_Pedro"
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
window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
window.fill((238, 238, 238))
X,Y = window.get_size()
pygame.display.update()

###############
## VARIABLES ##
###############

pag_count=0 #Indicates in wich page of the protocol we are located
participant_code = "" #Input text variable for participant code
input_rect = pygame.Rect(0,0,500,500) #Rectangle for input text
title_font = pygame.font.Font(None,60) #Title font
input_font = pygame.font.Font(None,32) #Body text font
time_font = pygame.font.Font(None, 100) #Time counter font
saved_words = [] #List with words saved
current_word = "" #Input text variable for currently wrinting use
N_words = 0 #Number of words saved on 'saved_words'
line = 25

output = [] #Output array
dt= "Date: " + str(datetime.datetime.now())
header = [dt]


while True: #permanently running
    if pag_count == 0: #PARTICIPANT CODE INPUT
        window.fill((238, 238, 238))

        text_surface = title_font.render("Codigo de participante: ", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, Y/2-100))

        text_surface2 = input_font.render(participant_code, True, (74,64,103))
        window.blit(text_surface2, (X/2-text_surface2.get_width()/2,Y/2))

        text_surface3 = input_font.render("Presioná 'Enter' para avanzar.", True, (74,64,103))
        window.blit(text_surface3, (X/2-text_surface3.get_width()/2,Y-100))


    if pag_count == 1: #INSTRUCTIONS
        window.fill((238, 238, 238))

        text_surface = title_font.render("INSTRUCCIONES:", True, (234, 64, 142))
        window.blit(text_surface, (X/2-text_surface.get_width()/2, 2*line))

        text_surface2 = input_font.render("Te pedimos que escribas 10 palabras que sean lo más diferente posible entre ellas, teniendo en cuenta sus significados y usos.", True, (74,64,103))
        window.blit(text_surface2, (line,Y/2-6*line))
        
        text_surface3 = input_font.render("Por favor, respetá las siguientes reglas:", True, (74,64,103))
        window.blit(text_surface3, (line,Y/2-5*line))
        
        text_surface4 = input_font.render("-Deben ser palabaras únicas, no compuestas", True, (74,64,103))
        window.blit(text_surface4, (2*line,Y/2-3*line))
        
        text_surface5 = input_font.render("-Solo usar sustantivos (ej., no es válido usar adjetivos o verbos)", True, (74,64,103))
        window.blit(text_surface5, (2*line,Y/2-2*line))
        
        text_surface6 = input_font.render("-No usar sustantivos propios (ej., no es válido usar nombres de personas o lugares)", True, (74,64,103))
        window.blit(text_surface6, (2*line,Y/2-line))
        
        text_surface7 = input_font.render("-No usar vocabulario especializado (ej., no es válido usar vocabulario técnico)", True, (74,64,103))
        window.blit(text_surface7, (2*line,Y/2))

        text_surface8 = input_font.render("-Finalmente te pedimos que te concentres en la pantalla, es decir, no intentes inspirarte usando pistas del ambiente donde estás.", True, (74,64,103))
        window.blit(text_surface8, (2*line,Y/2+line))

        text_surface9 = input_font.render("Vas a tener 3min para finalizar la tarea. Te avisaremos cuando te queden 30s.", True, (74,64,103))
        window.blit(text_surface9, (line,Y/2+3*line))

        text_surface10 = input_font.render("¡Esperamos tu mejor esfuerzo! Si se te acabó el tiempo y no enviaste respuestas, no te preocupes.", True, (74,64,103))
        window.blit(text_surface10, (line,Y/2+4*line))

        text_surface11 = input_font.render("Quedaron guardadas las que llegaste a completar.", True, (74,64,103))
        window.blit(text_surface11, (line,Y/2+5*line))

        text_surface12 = input_font.render("Presioná 'Enter' para comenzar.", True, (74,64,103))
        window.blit(text_surface12, (X/2-text_surface12.get_width()/2,Y/2+11*line))

    if pag_count == 2: #DIVERGENT ASSOCIATION TASK
        window.fill((238, 238, 238))

        text_surface1 = input_font.render("1) ", True, (74,64,103))
        window.blit(text_surface1, (line, 100))

        text_surface2 = input_font.render("2) ", True, (74,64,103))
        window.blit(text_surface2, (line, 100+line))

        text_surface3 = input_font.render("3) ", True, (74,64,103))
        window.blit(text_surface3, (line, 100 + 2 *line))

        text_surface4 = input_font.render("4) ", True, (74,64,103))
        window.blit(text_surface4, (line, 100 + 3 *line))

        text_surface5 = input_font.render("5) ", True, (74,64,103))
        window.blit(text_surface5, (line, 100 + 4 *line))
        
        text_surface6 = input_font.render("6) ", True, (74,64,103))
        window.blit(text_surface6, (line, 100+ 5 * line))

        text_surface7 = input_font.render("7) ", True, (74,64,103))
        window.blit(text_surface7, (line, 100  + 6 *line))

        text_surface8 = input_font.render("8) ", True, (74,64,103))
        window.blit(text_surface8, (line, 100 + 7 *line))

        text_surface9 = input_font.render("9) ", True, (74,64,103))
        window.blit(text_surface9, (line, 100 + 8 *line))

        text_surface10 = input_font.render("10) ", True, (74,64,103))
        window.blit(text_surface10, (line, 100 + 9 *line))

        

        # if len(saved_words) > 0:
        #         for x in saved_words:

        
        
        text_surface2 = input_font.render(current_word, True, (74,64,103))
        window.blit(text_surface2,(line + text_surface10.get_width(), 100 + N_words*line))

        
    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if pag_count == 1 or pag_count == 0:
                    pag_count = pag_count + 1
                if pag_count == 2:
                    if len(current_word)>0:
                        saved_words.append(current_word)
                        output.append(current_word)
                        current_word = ""
                        N_words = N_words + 1
            elif event.key == pygame.K_ESCAPE:
                #close_eng()
                pygame.quit()
                sys.exit()
            else:
                if pag_count == 0:
                    participant_code += event.unicode
                if pag_count == 2 and N_words < 10:
                    current_word += event.unicode

        if event.type == pygame.QUIT: #If user quits.
            logging.debug(str(output))
            logging.debug(mess)
            #close_eng()
            pygame.quit()
            sys.exit()