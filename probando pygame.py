import pygame
import sys
import time 
 
pygame.init()
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

pagina=0
cuenta=3
cont_c=0
cont_a=0
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if pagina != 1:
                    pagina=pagina-1
            if event.key == pygame.K_RIGHT:
                pagina=pagina+1
            if event.key==pygame.K_q:
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if pagina==7:
        dialogue = dialogue_font.render("Terminaste",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))
        dialogue1 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
        dialogue2 = dialogue_font.render("Muchas gracias", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
    saltear=0
    if pagina ==6:
        if cont_a != 5:
            time.sleep(5)#abiertos
            soundObj.play()
            time.sleep(1) # wait and let the sound play for 1 second
        cont_a=cont_a+1
        print("abrio", cont_a, "veces")
        soundObj.stop()
        dialogue = dialogue_font.render("",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))
        dialogue1 = dialogue_font.render("Mantené tus ojos cerrados.", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
        dialogue2 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
        if cont_a==5:
            pagina=7
        else: 
            pagina=5
        saltear=1

    if pagina==5 and saltear==0:
        time.sleep(5)#Cerrados
        cont_c=cont_c+1
        print("cerro", cont_c, "veces")
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
        pagina=pagina+1

        dialogue = dialogue_font.render("Abrí los ojos y mantenelos abiertos.",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))        
        dialogue1 = dialogue_font.render("Al escuchar un sonido volvé cerrar los ojos.", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  
        dialogue2 = dialogue_font.render("Al escuchar un doble sonido abrilos.", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
                

    if pagina==4:
        soundObj = pygame.mixer.Sound('D:/Doctorado/Biosemi/tum.wav')
        soundObj.play()
        time.sleep(1) # wait and let the sound play for 1 second
        soundObj.stop()

        dialogue = dialogue_font.render("",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))

        dialogue1 = dialogue_font.render("Mantené tus ojos cerrados.", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  

        dialogue2 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea))
        pagina=pagina+1
        

    if pagina==3:

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
            pagina=pagina+1
            dialogue1 = dialogue_font.render("", True, (0,0,0))
            dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))
        cuenta=cuenta-1


    if pagina==2:
        
        dialogue = dialogue_font.render("Estás listo?",True, (0,0,0)) 
        dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))

        dialogue1 = dialogue_font.render("", True, (0,0,0))
        dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  

        dialogue2 = dialogue_font.render("Presione -> para continuar.  Q para salir.", True, (0,0,0))
        dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea)) 
    

    if pagina==1:
            
            dialogue = dialogue_font.render("En breve comenzará una cuenta regresiva. Al llegar a cero",True, (0,0,0)) 
            dialogue_rect = dialogue.get_rect(center = (X//2,Y//2-linea))

            dialogue1 = dialogue_font.render("y escuchar un sonido deberás cerrar los ojos.", True, (0,0,0))
            dialogue_rect1 = dialogue1.get_rect(center = (X//2,Y//2))  

            dialogue2 = dialogue_font.render("Al escuchar un doble sonido deberás abrirlos.", True, (0,0,0))
            dialogue_rect2 = dialogue2.get_rect(center = (X//2,Y//2+linea)) 


        
    screen.fill((255, 255, 255))
     
    screen.blit(dialogue, dialogue_rect)
    screen.blit(dialogue1, dialogue_rect1)
    screen.blit(dialogue2, dialogue_rect2)
     
    pygame.display.flip()
    clock.tick(60)