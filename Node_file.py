import pygame
import math

# Node class connecting all the truss elements
class node(pygame.sprite.Sprite):
	def __init__(self, x, y, canvas):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.screen = canvas
		

class beam_node(node):
	def __init__(self, x, y, canvas):
		node.__init__(self, x, y, canvas)
		self.rect = pygame.draw.circle(self.screen, [0,0,0], (self.x,self.y), 10)

	def update(self, pos=None):
		if pos == None:
			self.rect = pygame.draw.circle(self.screen, [0,0,0], (self.x,self.y), 10)
		else :
			dx = self.x-pos[0]
			dy = self.y-pos[1]
			self.rect.move(dx, dy)
			self.x = pos[0]
			self.y = pos[1]
			

class terrain_node(node):
	def __init__(self, x, y, canvas):
		node.__init__(self, x, y, canvas)
		self.foundation = pygame.image.load("static_node.png").convert_alpha()
		self.rect = self.foundation.get_rect()

	def update(self, pos=None):
		
		if pos == None:
			self.rect.center = (self.x, self.y)
			self.screen.blit(self.foundation, self.rect)
		else:
			self.x = pos[0]
			self.y = pos[1]
			self.rect = self.foundation.get_rect()
			self.rect.center = (self.x, self.y)
			self.screen.blit(self.foundation, self.rect)