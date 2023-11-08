import pygame
import math
import Node_file
import Beam_file
import Terrain_Blocks

pygame.init()

screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("Game Demo")

structure = []
node_list = []

# set up the pygame clock
clock = pygame.time.Clock()

# Basic state conditionals
run = True
draw = False

# Set up initial nodes
node_list.append(Node_file.terrain_node(200,200, screen))

# Set up the terrain layout
terr = Terrain_Blocks.terrain(1200,600)
terrain_list = [['LLC',(0,-50)]]
terrain_list.append(['LLF', (0,50)])
terrain_list.append(['BSF', (100,50)])
terrain_list.append(['LRF', (200,50)])
terrain_list.append(['LRC', (200,-50)])
terrain_list.append(['BSF', (300,-50)])
terrain_list.append(['LLC', (400,-50)])
terrain_list.append(['LLF', (400,50)])
terrain_list.append(['LLC', (500,50)])
terrain_list.append(['LLF', (500,150)])
terrain_list.append(['LRF', (600,150)])
terrain_list.append(['LRC', (600,50)])
terrain_list.append(['BSF', (700,50)])
terrain_list.append(['BSF', (800,50)])
terrain_list.append(['LRF', (900,50)])
terrain_list.append(['LRC', (900,-50)])
terrain_list.append(['BSF', (1000,-50)])
terrain_list.append(['BSF', (1100,-50)])
terr.set_terrain(terrain_list, screen)

while run:

	# Wipe the Screen
	screen.fill([255,255,255])
	
	# Update the terrain
	screen.blit(terr.floor_surface, (0,300))

	# process events looking for mouse related events or end condition
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        run = False
	    elif event.type == pygame.MOUSEMOTION:
	    	if(draw):
	    		structure[-1].update(pygame.mouse.get_pos())
	    elif event.type == pygame.MOUSEBUTTONUP :
	    	pos = pygame.mouse.get_pos()
	    	for x in node_list[:-1]:
	    		if x.rect.collidepoint(pos):
	    			node_list.pop()
	    			structure[-1].set_end_node(x)
	    			structure[-1].update(x.rect.center)
	    			draw = False
	    			continue
	    	origin = (0,0)
	    	draw = False
	    elif event.type == pygame.MOUSEBUTTONDOWN:
	    	pos = pygame.mouse.get_pos()
	    	# Check if location was inside another node and replace it
	    	for x in node_list:
	    		if x.rect.collidepoint(pos):
	    			draw = True
	    			node_list.append(Node_file.beam_node(pos[0],pos[1], screen))
	    			structure.append(Beam_file.beam(x.rect.center, x, screen, node_list))
	    			structure[-1].set_end_node(node_list[-1])
	    			# print(x.rect.center)
	    			break

	# Update the depiction of the whole structure    			
	for bm in structure:
		bm.update()
	for nd in node_list:
		nd.update()

	# refresh the screen
	pygame.display.update()
	clock.tick(60)

i=0
for nd in node_list:
	print(str(i) + " - " + str(nd.rect.center))
	i += 1
i=0
for md in structure:
	print("Beam " + str(i) + ": " + str(md.end_node) + " - " + str(md.start_node))
	i += 1
pygame.quit()
