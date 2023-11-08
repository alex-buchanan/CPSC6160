import pygame
import math

pygame.init()

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Game Demo")

clock = pygame.time.Clock()

run = True
	
position = (0,0)
last_pos = None
drawing = False

screen.fill([255,255,255])

while run:
	x,y = pygame.mouse.get_pos()

	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        run = False
	    elif event.type == pygame.MOUSEMOTION:
	    	if(drawing):
	    		mouse_loc = pygame.mouse.get_pos()
	    		if last_pos is not None :
	    			screen.fill([255,255,255])
	    			pygame.draw.line(screen, [0,0,0], last_pos, mouse_loc, 1)
	    elif event.type == pygame.MOUSEBUTTONUP :
	    	position = (0,0)
	    	drawing = False
	    elif event.type == pygame.MOUSEBUTTONDOWN:
	    	drawing = True
	    	last_pos = pygame.mouse.get_pos()

	    # print(pygame.event.event_name(event.type))

	pygame.display.update()
	clock.tick(60)

pygame.quit()
