# Importing pygame module
from itertools import count
import pygame
from pygame.locals import *
import sys
import time
import serial
from comunicacion import *
#100 gree, 170 blue, 255 start, 200 end
port='COM5'


# Initiate pygame
pygame.init()
#A mark is sent to the EEG indicating that the protocol has started.
send_mark_biosemi(port,255)
# create the display surface object
# of specific dimension.
window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)

# Fill the screen with white color
window.fill((255, 255, 255))
X,Y=window.get_size()
# Using draw.rect module of
# pygame to draw the solid circle
pygame.draw.circle(window, (0, 255, 0),[X//2, Y//2], 170, 0)

#we start to count the differents moments. count 1 and 3 will be blue (odd). 2 and 4 will be green (normal)
count=0
while True:
    if count==1:
        #at first we wait five seconds
        time.sleep(5)


    if count==1 or count==3:
        #we wait 5 seconds more and the we turn the ball into blue (odd)
        time.sleep(5)
        pygame.draw.circle(window, (0, 0, 255),[X//2, Y//2], 170, 0)
        print("blue")
        

    if count==2 or count==4:
        #we wait only 0.1 seconds and the ball turns green again (normal)
        time.sleep(0.1)
        pygame.draw.circle(window, (0, 255, 0),[X//2, Y//2], 170, 0)
        print("green")
        
    if count==5:
        #we quit de program five seconds after the ball turns green for the last time
        time.sleep(5)
        pygame.quit()
        sys.exit()
        
    if count==2 or count==4:
        #we send a mark to te EEG indicating wether the ball is green or blue
        send_mark_biosemi(port,100)#100=green
    if count==1 or count==3:
        send_mark_biosemi(port,170)#170=blue
    
    #we update the screen. Changes before mentioned will be only visible after this line
    pygame.display.update()


    count=count+1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_q:
                #the user can quit the protocol by pressing Q key
                #one last mark is sent indicating that the protocol is over
                send_mark_biosemi(port,200)
                pygame.quit()
                sys.exit()
    if event.type == pygame.QUIT:
        #one last mark is sent indicating that the protocol is over
        send_mark_biosemi(port,200)
        pygame.quit()
        sys.exit()
