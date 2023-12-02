import pygame
import copy
from pygame.math import Vector2
import math
import Terrain_Blocks
from Arrow import draw_arrow

#colors
WHITE = [255,255,255]
BLACK = [10,10,10]

class physics:
	def __init__(self, object_part, p0, v0, type_obj):
		self.obj = object_part
		self.mass = 0
		self.theta = 0
		self.omega = 0
		self.pos = Vector2(p0)
		self.vel = Vector2(v0)

		self.forces = Vector2()
		self.torque = 0

		# should be calculated from the mask?
		self.CG_point = Vector2()
		self.I = 0
		self.cntrd_to_obj = Vector2()

		self.type = type_obj

	def move(self, dt):
		# Need to create a list of all forces on the object and their locations
		collision = pygame.sprite.spritecollide(self.obj, self.obj.blck_grp, False, pygame.sprite.collide_mask)
		if collision :
			overlap_vec = Vector2()
			x_offset = collision[0].rect.x - self.obj.rect.x
			y_offset = collision[0].rect.y - self.obj.rect.y
			dx = self.obj.mask.overlap_area(collision[0].mask, (x_offset + 1, y_offset)) - self.obj.mask.overlap_area(collision[0].mask, (x_offset - 1, y_offset))
			dy = (self.obj.mask.overlap_area(collision[0].mask, (x_offset, y_offset + 1)) - self.obj.mask.overlap_area(collision[0].mask, (x_offset, y_offset - 1)))
			overlap_mask = self.obj.mask.overlap_mask(collision[0].mask, (x_offset,y_offset))
			overlap_centroid = overlap_mask.centroid()
			self.cntrd_to_obj = self.pos - Vector2(overlap_centroid[0]+self.obj.rect.x, overlap_centroid[1]+self.obj.rect.y)
			
			# Move the obj until it no longer collides with this object
			self.pos += -self.vel*dt
			
			# while dx != 0 or dy != 0:
			# 	d_p = Vector2(dx,dy)
			# 	self.pos += d_p.normalize()
			# 	self.obj.rect.center = self.pos
			# 	x_offset = collision[0].rect.x - self.obj.rect.x
			# 	y_offset = collision[0].rect.y - self.obj.rect.y
			# 	dx = self.obj.mask.overlap_area(collision[0].mask, (x_offset + 1, y_offset)) - self.obj.mask.overlap_area(collision[0].mask, (x_offset - 1, y_offset))
			# 	dy = self.obj.mask.overlap_area(collision[0].mask, (x_offset, y_offset + 1)) - self.obj.mask.overlap_area(collision[0].mask, (x_offset, y_offset - 1))
			self.vel += 1.5*self.vel.magnitude()*self.cntrd_to_obj.normalize()
		self.update(dt)
		self.obj.rect.center = self.pos

	def update(self, dt):
		self.vel += self.forces*dt 
		self.pos += self.vel*dt 

		self.omega += self.torque*dt 
		self.theta += self.omega*dt 

class block(pygame.sprite.Sprite):
	def __init__(self, canvas):
		super().__init__()
		self.phy = physics(self, (300,300), (0,0), "beam")

		self.screen = canvas

		self.image = pygame.Surface((40,40), pygame.SRCALPHA)
		self.image.fill(WHITE)

		self.overlap_centroid = Vector2()

		self.rect = self.image.get_rect(center=self.phy.pos)
		pygame.draw.line(self.image, BLACK, (0,0) , (self.rect.width,self.rect.height), 4)
		self.mask = pygame.mask.from_threshold(self.image, BLACK, BLACK)

	def update(self):
		self.screen.blit(self.image, self.rect)

class car(pygame.sprite.Sprite):
	def __init__(self, canvas, blockgroup):
		super().__init__()

		# kinematic variables
		# self.pos = Vector2(40,0)
		# self.vel = Vector2(10,10)

		# Physics Engine
		self.phy = physics(self, (20,300), (10,0), "ball")

		self.blck_grp = blockgroup
		
		self.image = pygame.Surface((40,40), pygame.SRCALPHA)
		self.image.fill(WHITE)

		self.rect = self.image.get_rect(center=self.phy.pos)
		pygame.draw.circle(self.image, BLACK, (20,20), 20)

		self.image.set_colorkey(WHITE)
		self.mask = pygame.mask.from_threshold(self.image,BLACK, BLACK)
		
		self.force_total = Vector2(0,0)
		self.mass = 300

		self.screen = canvas

	def update(self):
		self.mask = pygame.mask.from_threshold(self.image,BLACK, BLACK)
		self.screen.blit(self.image, self.rect)
		# draw_arrow(self.screen, self.phy.pos, self.phy.vel+self.phy.pos, WHITE, 5, 10, 5)
		if self.phy.cntrd_to_obj.x != 0:
			draw_arrow(self.screen, self.phy.pos, -self.phy.cntrd_to_obj+self.phy.pos, (255,0,0), 5, 10, 5)

def main():
	global START_SIM

	screen = pygame.display.set_mode((1200,600))
	pygame.display.set_caption("Game Demo")

	# set up the pygame clock
	clock = pygame.time.Clock()

	block_G = pygame.sprite.Group()
	block_G.add(block(screen))

	# Basic state conditionals
	run = True

	# Object
	ball = car(screen, block_G)
	dt = 10

	while run:
		screen.fill(WHITE)

		# process events looking for mouse related events or end condition
		for event in pygame.event.get():
		    x,y = pygame.mouse.get_pos()
		    if event.type == pygame.QUIT:
		        run = False

		for i in range(100):
			ball.phy.move(dt/12000)

		block_G.update()
		ball.update()
		

		# refresh the screen
		pygame.display.update()
		dt = clock.tick(120)

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
