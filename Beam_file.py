import pygame
import math

# Beam class showing connecting elements in structure
class beam(pygame.sprite.Sprite):
	### Constructor that sets up all of the relevant variables
	def __init__(self, origin, node, canvas, list_n):
		pygame.sprite.Sprite.__init__(self)
		self.beam_image = pygame.image.load("Trunk_2.png").convert_alpha()
		self.x1 = origin[0]
		self.y1 = origin[1]
		self.length = 0
		self.rad_alpha = 0
		self.alpha = 0
		self.node_list = list_n
		self.start_node = self.node_list.index(node)
		self.background = canvas

	### Sets or modifies the index to be used as a reference for the last node
	def set_end_node(self,node):
		self.end_node = self.node_list.index(node)
	
	### Updates the visual appearance of the beam on the screen
	def update(self,mouse_pos = None):
		if mouse_pos is not None:
			#clear the previous draw

			# set up the x and y delta
			dx = mouse_pos[0] - self.x1
			dy = self.y1 - mouse_pos[1]

			# get the angle of the line between mouse and origin
			self.rad_alpha = math.atan2(dx,dy) - math.pi/2
			self.alpha = -180/math.pi * self.rad_alpha

			# get length of the beam to render
			self.length = int(math.sqrt(dx**2 + dy**2))
		
		# Render the beam all along the length of the line connecting the two nodes
		for x in range(0,self.length):
			beam = pygame.transform.scale(self.beam_image, (1,10))
			beam = pygame.transform.rotate(beam, self.alpha)
			rect = beam.get_rect(center=(self.x1+int(x*math.cos(self.rad_alpha)), self.y1+int((x)*math.sin(self.rad_alpha))))
			self.background.blit(beam, rect)
			self.node_list[self.start_node].update()
			self.node_list[self.end_node].update((self.x1+int(self.length*math.cos(self.rad_alpha)), self.y1+int(self.length*math.sin(self.rad_alpha))))
