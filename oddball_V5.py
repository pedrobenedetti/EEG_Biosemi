#UPDATED 27/9/2022
#ODDBALL paradigm. This protocol consist in a ball that blinks green or red with a probability of 5/6 and 1/6, respectively.
# User must press a button each time he sees a red ball
#matlab_parallel_com.py and send_mark_matlab.m files are needed. lib of matlab must be placed in folder. MATLAB-Python communication must be installed. Python 3.7 or older is needed.
import pygame
from pygame.locals import *
import sys
import datetime
import logging
import random

logging.basicConfig(filename="logger_oddball.txt", level=logging.DEBUG)
time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
mess0="\n Welcome to oddball pygame V4 protocol"
logging.debug(mess0)
mess=(time_txt + ": Initializing protocol...")
logging.debug(mess)

try:
    from matlab_parallel_com import *
    #imports script where MATLAB fuctions are defined. MATLAB engine will be started.
except:
    #throws an exception and message if some error ocurred.
    print("Can't import 'matlab_parallel_com'")
    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess=(time_txt + ": Can't import 'matlab_parallel_com'")
    logging.error(mess)

#Codes for marks: 
    # 25 start of code and start of protocol.
    # 75 ball turned into green.
    # 100 user press button.
    # 175 red.
    # 250 end of protocol.

#Codes for colors:
    #Green: (0,255,0)
    #red: (255,0,0)

port='C020'
#Defines parallel port name

pygame.init()
# Initiate pygame
try:
    send_mark_biosemi(20, port)
    #A mark (25) is sent to the EEG indicating that the code has started.
except:
    print("Can't execute 'send_mark_biosemi' properly")
    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
    logging.error(mess)


window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)


window.fill((255, 255, 255))
# Fill the screen with white color
line=50
X,Y=window.get_size()
dialogue_font = pygame.font.Font(None, line)
dialogue = dialogue_font.render("Por favor prestá atención a los estímulos que aparecen.", True, (0,0,0))
dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-line))
dialogue1 = dialogue_font.render("Presioná -> cada vez que veas una bola roja.", True, (0,0,0))
dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
dialogue2 = dialogue_font.render("Ahora, presioná -> para comenzar. Q para salir.", True, (0,0,0))
dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+1.5*line))

window.blit(dialogue, dialogue_rect)
window.blit(dialogue1, dialogue_rect1)
window.blit(dialogue2, dialogue_rect2)
pygame.display.update()

N_stim = 120 
#number of stimuli we want
period=1
#Time between consecutive stimuli (seconds)
duration_stim = 0.25 
#Duration of stimuli (seconds)
stim_counter = 0
#we start to count the stimuli.
frequent_counter = 0
#we will count how many green balls are showed
odd_counter = 0
#we will count how many red balls are showed
started = False
#Variable that indicates that the user has not yet started the protocol (pressed ->)
ball=0
#Variable taht indicates that an stimulus is being presented or not

while True:
    if started:
        time_now = datetime.datetime.now() 
        #Current time
        time_passed = (time_now-time_last).total_seconds() 
        #Time passed since last stimulus has been presented
        if ball == 1:
            if time_passed >= duration_stim:
                #If an stimulus is being showed and more than 'duration_stim' seconds have passed since it's appearance, screen will be cleaned.
                ball = 0
                window.fill((255, 255, 255))
                #screen is cleaned. Stimulus is ended.
                pygame.display.update()
                
        if time_passed > period:
            stim_counter = stim_counter + 1
            number = random.randint(1,6)
            if number >= 1 and number <= 5:
                #Ball will be green. frequent Stimulus.
                pygame.draw.circle(window, (0, 255, 0),[X//2, Y//2], 170, 0)
                pygame.display.update()
                ball = 1
                frequent_counter = frequent_counter + 1
                
                try:
                    send_mark_biosemi(75, port)
                    #75=turned into green
                except:
                    print("Can't execute 'send_mark_biosemi' properly")
                    time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    mess = (time_txt + ": Can't execute 'send_mark_biosemi' properly")
                    logging.error(mess)
                    
            if number == 6:
                #Ball will be red.
                pygame.draw.circle(window, (255, 0, 0),[X//2, Y//2], 170, 0)
                pygame.display.update()
                ball = 1
                odd_counter = odd_counter + 1
                print("se mostro el rojo a las", datetime.datetime.now())
                try:
                    send_mark_biosemi(175, port)
                    #175=turned into red. Rare stimulus.
                except:
                    print("Can't execute 'send_mark_biosemi' properly")
                    time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    mess = (time_txt + ": Can't execute 'send_mark_biosemi' properly")
                    logging.error(mess)
            
            time_last=datetime.datetime.now()
    while not started:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    started = 1
                    #This means that the user has started the protocol
                    print("Empezo")
                    time_last=datetime.datetime.now() 
                    #Initial Time. Afterwards protocol has started this will indicate the last time a stimulus has been presented.
                    window.fill((255, 255, 255))
                    pygame.display.update()
                    try:
                        send_mark_biosemi(25, port)
                        #A mark (25) is sent to the EEG indicating that the protocol has started.
                    except:
                        print("Can't execute 'send_mark_biosemi' properly")
                        time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                        mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
                        logging.error(mess)
                    break

    
    #checks if the protocol has to end
    if stim_counter > N_stim:
        print(stim_counter, " stimuli have been showed.")
        print(frequent_counter, " frequent stimuli have been showed.")
        print(odd_counter, " odd stimuli have been showed.")
        try:
        #one last mark is sent indicating that the protocol is over
            send_mark_biosemi(250, port)
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Ending protocol..."+"\n")
            logging.debug(mess)
        except:
            print("Can't execute 'send_mark_biosemi' properly")
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
            logging.error(mess)
        #Closes MATLAB engine
        close_eng()
        #Quits pygame
        pygame.quit()
        #Closes the window
        sys.exit()
        
    #Updates the screen. Changes before mentioned will be only visible after this line. Note that this is executed permanently after each cycle.
    pygame.display.update()
    
    #The user can also finish the protocol by pressing 'Q' key.
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_q:
                #the user can quit the protocol by pressing Q key
                try:
                #one last mark is sent indicating that the protocol is over
                    send_mark_biosemi(250, port)
                    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    mess=(time_txt + ": Ending protocol..."+"\n")
                    logging.debug(mess)
                except:
                    print("Can't execute 'send_mark_biosemi' properly")
                    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
                    logging.error(mess)
                close_eng()
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RIGHT:
                print("apreto el boton a las", datetime.datetime.now())
                try:
                    send_mark_biosemi(100, port)
                    #User pressed right button
                except:
                    print("Can't execute 'send_mark_biosemi' properly")
                    time_txt = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    mess = (time_txt + ": Can't execute 'send_mark_biosemi' properly")
                    logging.error(mess)
                    
    if event.type == pygame.QUIT:
        try:
            #one last mark is sent indicating that the protocol is over
            send_mark_biosemi(250, port)
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Ending protocol..."+"\n")
        except:
            print("Can't execute 'send_mark_biosemi' properly")
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
            logging.error(mess)
        logging.debug(mess)
        close_eng()
        pygame.quit()
        sys.exit()
