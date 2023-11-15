import pygame
import copy
from pygame.math import Vector2
import math
import Terrain_Blocks

#colors
WHITE = [255,255,255]
BLACK = [10,10,10]

# Constants
G = Vector2(0,2)
START_SIM = False

class node(pygame.sprite.Sprite):
	def __init__(self, x, y, canvas, group=None, fixed=False):
		
		if group is not None:
			super().__init__(group)
		else:
			super().__init__()
		
		# kinematic variables
		self.pos = Vector2(x,y)
		self.vel = Vector2(0,0)
		self.fixed = fixed
		
		self.image = pygame.Surface((20,20), pygame.SRCALPHA)
		self.image.fill(WHITE)
		self.canvas = canvas
		self.rect = self.image.get_rect(center=self.pos)
		pygame.draw.circle(self.image, BLACK, (10,10), 10)
		self.image.set_colorkey(WHITE)
		self.mask = pygame.mask.from_surface(self.image)
		
		self.force_total = Vector2()
		self.ground_force = Vector2()
		self.terr_list = []
		self.mass = 5
		self.vec_list = []

	def run_sim(self,dt,terr):
		global G
		if not self.fixed:
			# Use Euler's Method for now
			self.force_total = G*self.mass

			# Sum all of the force vectors acting on this particular node
			for b in self.vec_list:
				n_i = b.nodes.index(self)
				magnitude = (b.L0 - b.length)*b.k
				if not n_i:
					self.force_total += -magnitude*b.dir_vec.normalize() - self.vel*b.c
				else:
					self.force_total += magnitude*b.dir_vec.normalize() - self.vel*b.c

			# Check if the node has bumped up against the ground and negate
			#   the forces in that direction:
			self.terr_list.clear()
			self.terr_list.extend(pygame.sprite.spritecollide(self, terr.terrain_list, False, pygame.sprite.collide_mask))
			vel_vec = Vector2()
			if len(self.terr_list):
				for t in self.terr_list:
					self_point = pygame.sprite.collide_mask(self, t)
					if self_point is not None:
						sur_vec = Vector2(self_point) - Vector2(10,10)
						self.vel = -self.vel.project(sur_vec)
						self.pos += self.vel*dt
						self.update(self.pos)
					else :
						self.vel += (self.force_total/self.mass)*dt
						self.pos += self.vel*dt
						self.update(self.pos)
			else:
				self.vel += (self.force_total/self.mass)*dt
				self.pos += self.vel*dt
				self.update(self.pos)
		
	def update(self, mouse_pos=None):
		if mouse_pos is not None:
			self.pos.update(mouse_pos)
			self.rect.center = self.pos
		self.canvas.blit(self.image, self.rect)

	def add_beam_ref(self, beam):
		self.vec_list.append(beam)



class beam(pygame.sprite.Sprite):
	def __init__(self, a_node, b_node, group, canvas):
		super().__init__(group)

		self.nodes = [a_node, b_node]
		
		self.dir_vec = self.nodes[1].pos - self.nodes[0].pos
		self.L0 = self.dir_vec.magnitude()
		self.length = self.L0
		
		self.canvas = canvas
		self.image = pygame.Surface((abs(self.nodes[0].pos.x-self.nodes[1].pos.x),abs(self.nodes[0].pos.y-self.nodes[1].pos.y)), pygame.SRCALPHA)
		self.rect = self.image.get_rect(center=(self.nodes[0].pos+self.nodes[1].pos)/2)
		
		a_node.add_beam_ref(self)
		b_node.add_beam_ref(self)

		# Spring constant
		self.k = 50
		self.c = .25

	def move(self, mouse_pos):
		global START_SIM
		
		self.dir_vec.update(self.nodes[1].pos - self.nodes[0].pos)
		self.length = self.dir_vec.magnitude()

		self.image = pygame.transform.scale(self.image, (abs(self.nodes[0].pos.x-self.nodes[1].pos.x)+5,abs(self.nodes[0].pos.y-self.nodes[1].pos.y)+5))
		self.rect.center = ((self.nodes[0].pos.x+self.nodes[1].pos.x)/2, (self.nodes[1].pos.y+self.nodes[0].pos.y)/2)
		
		if not START_SIM:
			self.L0 = self.dir_vec.magnitude()

	def update(self):
		self.nodes[0].update()
		self.nodes[1].update()

		x0, y0 = self.nodes[0].pos
		x1, y1 = self.nodes[1].pos

		self.rect.width = abs(x0-x1)+5
		self.rect.height = abs(y0-y1)+5
		self.rect.center = ((x0+x1)/2, (y1+y0)/2)

		self.dir_vec.update(self.nodes[1].pos - self.nodes[0].pos)

		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)

		pygame.draw.line(self.image, BLACK, (x0-self.rect.x , y0-self.rect.y), (x1-self.rect.x, y1-self.rect.y), 5)
		self.canvas.blit(self.image, self.rect)
		
		self.mask = pygame.mask.from_surface(self.image)

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

class car(pygame.sprite.Sprite):
	def __init__(self, x, y, screen):
		super().__init__()
		# kinematic variables
		self.pos = Vector2(x,y)
		self.vel = Vector2(.25,0)
		
		self.image = pygame.Surface((40,40), pygame.SRCALPHA)
		self.image.fill(WHITE)
		self.rect = self.image.get_rect(center=self.pos)
		pygame.draw.circle(self.image, BLACK, (20,20), 20)
		self.image.set_colorkey(WHITE)
		self.mask = pygame.mask.from_surface(self.image)
		
		self.force_total = Vector2(0,0)
		self.mass = 50

		self.screen = screen

	def update(self):
		self.screen.blit(self.image, self.rect)

	def simulate(self,beams,terr,dt):
		global G
		self.force_total = G*self.mass

		# Check if the node has bumped up against the ground and negate
		#   the forces in that direction:
		t_list = pygame.sprite.spritecollide(self, terr.terrain_list, False, pygame.sprite.collide_mask)
		b_list = pygame.sprite.spritecollide(self, beams, False, pygame.sprite.collide_mask)

		force_vec = Vector2((0,0))
		vel_vec = Vector2((0,0))

		if len(t_list):
			#print(len(t_list))
			for t in t_list:
				x_offset = t.rect.x-self.rect.x 
				y_offset = t.rect.y-self.rect.y
				self_point = Vector2(pygame.sprite.collide_mask(self, t))
				sur_vec = -Vector2(Vector2((20,20))-self_point)

				mag_in_surface = self.force_total.dot(sur_vec.normalize())
				force_vec += mag_in_surface*sur_vec.normalize()

				vel_mag = self.vel.dot(sur_vec.normalize())
				vel_vec += vel_mag*sur_vec.normalize()

			self.force_total -= force_vec
			self.vel += -.5*vel_vec + (self.force_total/self.mass)*dt
			self.pos += self.vel*dt - 2*sur_vec.normalize()
			self.rect.center = self.pos
		else:
			self.vel += (self.force_total/self.mass)*dt
			self.pos += self.vel*dt
			self.rect.center = self.pos

		force_vec = Vector2((0,0))
		vel_vec = Vector2((0,0))

		if len(b_list) and b_list is not None:
			#print("b_list length: ",len(b_list))
			for t in b_list:
				x_offset = t.rect.x-self.rect.x 
				y_offset = t.rect.y-self.rect.y
				#print("beam mask collide: ",pygame.sprite.collide_mask(self, t))
				self_point = pygame.sprite.collide_mask(self, t)
				if self_point is not None:
					sur_vec = -Vector2(Vector2((20,20)) - Vector2(self_point))

					mag_in_surface = self.force_total.dot(sur_vec.normalize())
					force_vec += mag_in_surface*sur_vec.normalize()

					vel_mag = self.vel.dot(sur_vec.normalize())
					vel_vec += vel_mag*sur_vec.normalize()

					self.force_total -= force_vec
					self.vel += -.5*vel_vec + (self.force_total/self.mass)*dt
					self.pos += self.vel*dt - 2*sur_vec.normalize()
					self.rect.center = self.pos
				else:
					self.vel += (self.force_total/self.mass)*dt
					self.pos += self.vel*dt
					self.rect.center = self.pos

		else:
			self.vel += (self.force_total/self.mass)*dt
			self.pos += self.vel*dt
			self.rect.center = self.pos


def main():
	global START_SIM

	screen = pygame.display.set_mode((1200,600))
	pygame.display.set_caption("Game Demo")

	# Set up the terrain layout
	terr = Terrain_Blocks.terrain(1200,600)
	terrain_list = [['LLC', (0,0)]]
	terrain_list.append(['RSF', (0,50)])
	terrain_list.append(['LLF', (0,100)])
	terrain_list.append(['BSF', (50,100)])
	terrain_list.append(['BSF', (100,100)])
	terrain_list.append(['BSF', (150,100)])
	terrain_list.append(['LRF', (200,100)])
	terrain_list.append(['LSF', (200,50)])
	terrain_list.append(['LRC', (200,0)])
	terrain_list.append(['BSF', (250,0)])
	terrain_list.append(['BSF', (300,0)])
	terrain_list.append(['BSF', (350,0)])
	terrain_list.append(['LLC', (400,0)])
	terrain_list.append(['RSF', (400,50)])
	terrain_list.append(['LLF', (400,100)])
	terrain_list.append(['BSF', (450,100)])
	terrain_list.append(['LLC', (500,100)])
	terrain_list.append(['LLF', (500,150)])
	terrain_list.append(['BSF', (550,150)])
	terrain_list.append(['LRF', (600,150)])
	terrain_list.append(['LRC', (600,100)])
	terrain_list.append(['BSF', (650,100)])
	terrain_list.append(['BSF', (700,100)])
	terrain_list.append(['BSF', (750,100)])
	terrain_list.append(['BSF', (800,100)])
	terrain_list.append(['BSF', (850,100)])
	terrain_list.append(['LRF', (900,100)])
	terrain_list.append(['LSF', (900,50)])
	terrain_list.append(['LRC', (900,0)])
	terrain_list.append(['BSF', (950,0)])
	terrain_list.append(['BSF', (1000,0)])
	terrain_list.append(['BSF', (1050,0)])
	terrain_list.append(['BSF', (1100,0)])
	terrain_list.append(['BSF', (1150,0)])
	
	
	# set up the pygame clock
	clock = pygame.time.Clock()

	# Simulation button setup
	sim_rect = pygame.Rect(900, 10, 200, 50)
	sim_button = button(sim_rect, "Simulate", screen)

	# Node group and initial nodes
	node_list = pygame.sprite.Group()

	foundation0 = node(50,300,screen,node_list,True)
	foundation1 = node(screen.get_width()/3, screen.get_height()/2, screen, node_list, True)
	foundation2 = node(1000, screen.get_height()/2, screen, node_list, True)

	# Beam group
	beam_list = pygame.sprite.Group()

	# Car
	vehicle = car(20,280,screen)

	# Basic state conditionals
	run = True
	draw = False
	new_node = None
	new_beam = None

	terr.set_terrain(terrain_list, screen)



	while run:
		screen.fill(WHITE)
		sim_button.render()

		# Update the terrain
		terr.render_terrain(screen)

		# Render the car
		vehicle.update()

		# process events looking for mouse related events or end condition
		for event in pygame.event.get():
		    x,y = pygame.mouse.get_pos()
		    if event.type == pygame.QUIT:
		        run = False
		    elif event.type == pygame.MOUSEMOTION and not START_SIM:
		    	if(draw):
		    		# Check for floor collision
		    		curr = new_node.pos
		    		new_beam.nodes[1].update((x,y))
		    		new_beam.move((x,y))
		    		if pygame.sprite.spritecollide(new_node, terr.terrain_list, False, pygame.sprite.collide_mask):
		    			new_beam.nodes[1].update(curr)
		    			new_beam.move(curr)
	    			
		    elif event.type == pygame.MOUSEBUTTONUP :
		    	if(draw):
		    		test_node = None
		    		for z in node_list:
		    			if z.rect.collidepoint((x,y)):
		    				test_node = z
		    				break
		    		if test_node is not None:
		    			if test_node is not new_beam.nodes[0]:
		    				new_beam.nodes[1] = test_node
		    				test_node.add_beam_ref(new_beam)
		    			else:
		    				beam_list.remove(new_beam)
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
			    		break
			    	# Check if location was inside another node and replace it
			    	anchor_node = None
			    	for z in node_list:
		    			if z.rect.collidepoint((x,y)):
		    				anchor_node = z
		    				break
			    	if anchor_node is not None:
			    		draw = True
			    		new_node = node(x,y,screen)
			    		new_beam = beam(anchor_node, new_node, beam_list, screen)

		if START_SIM:
			for i in range(100):
				for n in node_list:
					n.run_sim(dt,terr)
				for b in beam_list:
					b.move(b.nodes[1].pos)
				# vehicle.simulate(beam_list,terr,dt)

		
		node_list.update()
		beam_list.update()

		beam_list.draw(screen)
		node_list.draw(screen)

		# refresh the screen
		pygame.display.update()
		dt = clock.tick(60)/1000

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
