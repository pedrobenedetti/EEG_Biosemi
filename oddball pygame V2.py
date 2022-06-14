import pygame
from pygame.locals import *
import sys
import datetime
import logging
logging.basicConfig(filename="logger_oddball.txt", level=logging.DEBUG)
time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
mess0="\n Welcome to oddball pygame V2 protocol"
logging.debug(mess0)
mess=(time_txt + ": Initializing protocol...")
logging.debug(mess)

try:
    from parallel_com import *
except:
    print("Can't import 'parallel_com'")
    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess=(time_txt + ": Can't import 'parallel_com'")
    logging.error(mess)



#100 green, 170 blue, 255 start, 200 end
port='0xC020'

pygame.init()
# Initiate pygame
try:
    send_mark_biosemi(port,255)
    #A mark is sent to the EEG indicating that the protocol has started.
except:
    print("Can't execute 'send_mark_biosemi' properly")
    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
    logging.error(mess)


window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
# create the display surface object
# of specific dimension.

window.fill((255, 255, 255))
# Fill the screen with white color

X,Y=window.get_size()
pygame.draw.circle(window, (0, 255, 0),[X//2, Y//2], 170, 0)
# Using draw.rect module of
# pygame to draw the solid circle

Ncycles=5 
#number of cycles we want
duration_normal=5 
#Duration of normal stimulus (seconds)
duration_odd=0.1 
#duration of odd stimulus (seconds)
duration=duration_normal+duration_odd 
#total duration of cycle
restore=0 
#Indicate if turning green is needed
counter=0
#we start to count the cycles.
time0=datetime.datetime.now() 
#Initial Time

while True:
    time_now=datetime.datetime.now() 
    #Current Time
    time_passed=(time_now-time0).total_seconds() 
    #Seconds passed since initial time 

    if time_passed > (1+counter)*duration_normal+duration_odd*counter: 
        #We check if we have to turn blue the ball. It will happen every 'duration_normal' seconds
        pygame.draw.circle(window, (0, 0, 255),[X//2, Y//2], 170, 0) 
        #We turn the ball blue
        time_odd=datetime.datetime.now() 
        #We ask for the time
        print("Turned blue at ", time_passed, "seconds") 
        #Print message
        restore=1 
        #We indicate that we have to turn the ball green
        counter=counter+1
        try:
            send_mark_biosemi(port,170)
            #170=blue
        except:
            print("Can't execute 'send_mark_biosemi' properly")
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
            logging.error(mess)

    if restore==1: 
        #Ask if we have to restore the color to normal
        if (time_now-time_odd).total_seconds()>duration_odd: 
            #ask if 'duration_odd' seconds have passed since turning blue
            pygame.draw.circle(window, (0, 255, 0),[X//2, Y//2], 170, 0) 
            #Restore de color
            restore=0 
            #Reset 'restore'
            print("Turned green at ", time_passed, "seconds") 
            #Print message
            try:
                send_mark_biosemi(port,100)
                #100=green
            except:
                print("Can't execute 'send_mark_biosemi' properly")
                time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
                logging.error(mess)
        
    if counter>=Ncycles and time_passed>(1+Ncycles)*5+0.1*Ncycles:
        print("Ended at ", time_passed, "seconds")
        pygame.quit()
        sys.exit()
            
    pygame.display.update()
    #we update the screen. Changes before mentioned will be only visible after this line

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_q:
                #the user can quit the protocol by pressing Q key
                try:
                #one last mark is sent indicating that the protocol is over
                    send_mark_biosemi(port,200)
                    mess=(time_txt + ": Ending protocol..."+"\n")
                    logging.debug(mess)
                except:
                    print("Can't execute 'send_mark_biosemi' properly")
                    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
                    logging.error(mess)
                pygame.quit()
                sys.exit()
    if event.type == pygame.QUIT:
        try:
            #one last mark is sent indicating that the protocol is over
            send_mark_biosemi(port,200)
            mess=(time_txt + ": Ending protocol..."+"\n")
        except:
            print("Can't execute 'send_mark_biosemi' properly")
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Can't execute 'send_mark_biosemi' properly")
            logging.error(mess)
        logging.debug(mess)
        pygame.quit()
        sys.exit()