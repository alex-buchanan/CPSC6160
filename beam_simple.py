import pygame
import copy
from pygame.math import Vector2
import math
import Terrain_Blocks

#colors
WHITE = [255,255,255]
BLACK = [10,10,10]

# Constants
G = Vector2(0,4)
START_SIM = False
NODE_NUM = 0
BEAM_NUM = 0

class node(pygame.sprite.Sprite):
	def __init__(self, x, y, canvas, group=None, fixed=False):
		global NODE_NUM
		self.node_num = NODE_NUM
		NODE_NUM += 1
		if group is not None:
			super().__init__(group)
		else:
			super().__init__()
		# kinematic variables
		self.pos = Vector2(x,y)
		self.vel = Vector2(0,0)
		self.fixed = fixed
		self.image = pygame.Surface((20,20), pygame.SRCALPHA)
		self.canvas = canvas
		self.rect = self.image.get_rect(center=self.pos)
		pygame.draw.circle(self.image, BLACK, (10,10), 10)
		self.force_total = Vector2(0,0)
		self.mass = 2
		self.vec_list = []

	def run_sim(self,dt):
		global G
		if not self.fixed:
			# Use Euler's Method for now
			self.force_total = Vector2(G*self.mass)
			# self.vel = Vector2(0,0)
			for b in self.vec_list:
				# print("Node #: ",self.node_num)
				# print("Beam #: ", b.beam_num)
				n_i = b.nodes.index(self)
				if not n_i:
					reaction = -Vector2(b.dir_vec.normalize())
				else:
					reaction = Vector2(b.dir_vec.normalize())
				magnitude = (b.L0 - b.length)*b.k
				self.force_total += magnitude*reaction

			self.vel += (self.force_total/self.mass)*dt
			self.pos += self.vel*dt

	def move(self,mouse_pos):
		pygame.draw.circle(self.image, BLACK, (10,10), 10)
		self.pos = mouse_pos
		self.rect.center = self.pos

	def update(self):
		self.canvas.blit(self.image, self.rect)

	def add_beam_ref(self, beam):
		self.vec_list.append(beam)



class beam(pygame.sprite.Sprite):
	def __init__(self, a_node, b_node, group, canvas):
		super().__init__(group)
		global BEAM_NUM
		self.beam_num = BEAM_NUM
		BEAM_NUM += 1
		self.vec0 = Vector2()
		self.vec1 = Vector2()
		self.vec0.xy = a_node.pos
		self.vec1.xy = b_node.pos
		self.dir_vec = self.vec1 - self.vec0
		self.L0 = self.dir_vec.magnitude()
		self.length = self.L0
		self.canvas = canvas
		self.image = pygame.Surface((abs(self.vec0.x-self.vec1.x),abs(self.vec0.y-self.vec1.y)), pygame.SRCALPHA)
		self.rect = self.image.get_rect(center=(self.vec0+self.vec1)/2)
		a_node.add_beam_ref(self)
		b_node.add_beam_ref(self)
		self.nodes = [a_node, b_node]

		# Spring constant
		self.k = 0.5
		self.L0 = Vector2.length(self.dir_vec)

	def move(self, mouse_pos):
		global START_SIM
		
		self.nodes[1].move(mouse_pos)
		self.vec0.xy = self.nodes[0].pos 
		self.vec1.xy = self.nodes[1].pos
		
		self.dir_vec = self.vec1 - self.vec0
		self.length = self.dir_vec.magnitude()

		self.image = pygame.transform.scale(self.image, (abs(self.vec0.x-self.vec1.x)+5,abs(self.vec0.y-self.vec1.y)+5))
		self.rect = self.image.get_rect(center=((self.vec0.x+self.vec1.x)/2, (self.vec1.y+self.vec0.y)/2))
		
		if not START_SIM:
			self.L0 = Vector2.length(self.dir_vec)

	def update(self):
		self.nodes[0].update()
		self.nodes[1].update()
		x0, y0 = self.nodes[0].rect.center 
		x1, y1 = self.nodes[1].rect.center
		self.image = pygame.transform.scale(self.image, (abs(x0-x1)+5,abs(y0-y1)+5))
		self.rect = self.image.get_rect(center=((x0+x1)/2, (y1+y0)/2))
		self.dir_vec = self.vec1 - self.vec0
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		line_rect = pygame.draw.line(self.image, BLACK, (x0-self.rect.x , y0-self.rect.y), (x1-self.rect.x, y1-self.rect.y), 5)
		self.canvas.blit(self.image, self.rect)

class button :
	def __init__(self, rect, text, canvas):
		smallfont = pygame.font.SysFont('Corbel',35)
		self.text = smallfont.render(text , True , BLACK)
		self.text_a = smallfont.render(text , True , WHITE)
		self.txt_rect_center = self.text.get_rect(center=(rect.width/2, rect.height/2))
		self.rect = rect
		self.img = pygame.Surface((self.rect.width+5, self.rect.height+5), pygame.SRCALPHA)
		self.canvas = canvas

	def render(self):
		self.img.fill(WHITE)
		pygame.draw.rect(self.img, BLACK, pygame.Rect(0,0,self.rect.width, self.rect.height), 2)
		self.img.blit(self.text, self.txt_rect_center)
		self.canvas.blit(self.img, self.rect)

	def activate(self):
		self.img.fill(BLACK)
		self.img.blit(self.text_a, self.txt_rect_center)
		self.canvas.blit(self.img, self.rect)
		global START_SIM
		START_SIM = True

def main():
	global START_SIM

	screen = pygame.display.set_mode((1200,600))
	pygame.display.set_caption("Game Demo")

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
	
	
	# set up the pygame clock
	clock = pygame.time.Clock()

	sim_rect = pygame.Rect(900, 10, 200, 50)
	sim_button = button(sim_rect, "Simulate", screen)

	node_list = pygame.sprite.Group()

	foundation1 = node(screen.get_width()/3, screen.get_height()/2, screen, node_list, True)
	foundation2 = node(2*screen.get_width()/3, screen.get_height()/2, screen, node_list, True)

	beam_list = pygame.sprite.Group()

	# Basic state conditionals
	run = True
	draw = False
	new_node = None
	new_beam = None

	while run:
		screen.fill(WHITE)
		sim_button.render()

		# Update the terrain
		terr.set_terrain(terrain_list, screen)

		# process events looking for mouse related events or end condition
		for event in pygame.event.get():
		    x,y = pygame.mouse.get_pos()
		    if event.type == pygame.QUIT:
		        run = False
		    elif event.type == pygame.MOUSEMOTION and not START_SIM:
		    	if(draw):
		    		# Check for floor collision
		    		has_coll = False
		    		for t in terr.terrain_list:
		    			if t.block_s.collidepoint((x,y)):
		    				has_coll = True
		    				# print("collided")
		    				x1,y1 = t.image_s.get_offset()
		    				if not t.mask.get_at((x-x1,y-y1)):
		    					new_beam.move((x,y))
		    				# else:
		    				# 	print("local(x,y) = ("+str(x-x1)+","+str(y-y1)+")")
		    		if not has_coll:
		    			new_beam.move((x,y))
		    		# print("Mask Value = ",terr.terr_mask.get_at((x,y)))
		    		# if terr.terr_mask.get_at((x,y)) is 0:
		    		# new_beam.move((x,y))
		    elif event.type == pygame.MOUSEBUTTONUP :
		    	if(draw):
		    		test_node = None
		    		for z in node_list:
		    			if z.rect.collidepoint((x,y)):
		    				test_node = z
		    				break
		    		# test_node = pygame.sprite.spritecollideany(new_node, node_list, collided=None)
		    		if test_node is not None:
		    			print("Node on top of other detected.")
		    			new_beam.nodes[1] = test_node
		    			test_node.add_beam_ref(new_beam)
		    		else:
		    			new_node.add(node_list)
			    	new_beam = None
			    	new_node = None
			    	draw = False
		    elif event.type == pygame.MOUSEBUTTONDOWN and not START_SIM:
		    	if(not draw):
			    	# Check to activate sim
			    	if sim_rect.collidepoint((x,y)):
			    		sim_button.activate()
			    		print("Activated.")
			    		print(START_SIM)
			    		break
			    	# Check if location was inside another node and replace it
			    	anchor_node = None
			    	for z in node_list:
		    			if z.rect.collidepoint((x,y)):
		    				anchor_node = z
		    				break
			    	# anchor_node = pygame.sprite.spritecollideany(new_node, node_list, collided=None)
			    	if anchor_node is not None:
			    		draw = True
			    		new_node = node(x,y,screen)
			    		new_beam = beam(anchor_node, new_node, beam_list, screen)

		# if(new_beam is not None):
		# 	new_beam.update()

		if START_SIM:
			for n in node_list:
				# print(dt)
				n.run_sim(dt)
				n.move(n.pos)
			for b in beam_list:
				b.move(b.nodes[1].pos)

		
		node_list.update()
		beam_list.update()

		beam_list.draw(screen)
		node_list.draw(screen)

		# refresh the screen
		pygame.display.update()
		dt = clock.tick(240)/1000

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()