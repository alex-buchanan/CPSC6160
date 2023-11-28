import pygame
import copy
from pygame.math import Vector2
import math
import Terrain_Blocks

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

		self.CG_point = Vector2()
		self.I = 0

		self.type = type_obj

	def move(self, dt):
		collision = pygame.sprite.spritecollide(self.obj, self.obj.blck_grp, False, pygame.sprite.collide_mask)
		if collision :
			overlap_vec = Vector2()
			x_offset = collision[0].rect.x - self.obj.rect.x
			y_offset = collision[0].rect.y - self.obj.rect.y
			dx = self.obj.mask.overlap_area(collision[0].mask, (x_offset + 1, y_offset)) - self.obj.mask.overlap_area(collision[0].mask, (x_offset - 1, y_offset))
			dy = (self.obj.mask.overlap_area(collision[0].mask, (x_offset, y_offset + 1)) - self.obj.mask.overlap_area(collision[0].mask, (x_offset, y_offset - 1)))
			overlap_mask = self.obj.mask.overlap_mask(collision[0].mask, (x_offset,y_offset))
			overlap_centroid = overlap_mask.centroid()
			print(overlap_centroid[0]+collision[0].rect.x, overlap_centroid[1]+collision[0].rect.y)
			while dx != 0 or dy != 0:
				d_p = Vector2(dx,dy)
				self.pos += d_p.normalize()
				self.obj.rect.center = self.pos
				x_offset = collision[0].rect.x - self.obj.rect.x
				y_offset = collision[0].rect.y - self.obj.rect.y
				dx = self.obj.mask.overlap_area(collision[0].mask, (x_offset + 1, y_offset)) - self.obj.mask.overlap_area(collision[0].mask, (x_offset - 1, y_offset))
				dy = self.obj.mask.overlap_area(collision[0].mask, (x_offset, y_offset + 1)) - self.obj.mask.overlap_area(collision[0].mask, (x_offset, y_offset - 1))
				overlap_vec += d_p.normalize()
				print(dx,dy)
			print(overlap_vec)
			self.vel += 1.5*self.vel.reflect(overlap_vec)
			print(self.vel)
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
		self.pos = Vector2(300,300)

		self.screen = canvas

		self.image = pygame.Surface((40,40), pygame.SRCALPHA)
		self.image.fill(WHITE)

		self.rect = self.image.get_rect(center=self.pos)
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
		self.phy = physics(self, (20,20), (10,10),"ball")

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

	# def simulate(self, dt):
	# 	collision = pygame.sprite.spritecollide(self, self.blck_grp, False, pygame.sprite.collide_mask)
	# 	if collision :
	# 		overlap_vec = Vector2()
	# 		x_offset = collision[0].rect.x - self.rect.x
	# 		y_offset = collision[0].rect.y - self.rect.y
	# 		dx = self.mask.overlap_area(collision[0].mask, (x_offset + 1, y_offset)) - self.mask.overlap_area(collision[0].mask, (x_offset - 1, y_offset))
	# 		dy = -(self.mask.overlap_area(collision[0].mask, (x_offset, y_offset + 1)) - self.mask.overlap_area(collision[0].mask, (x_offset, y_offset - 1)))
	# 		while dx != 0 or dy != 0:
	# 			d_p = Vector2(dx,dy)
	# 			self.pos += d_p.normalize()
	# 			self.rect.center = self.pos
	# 			x_offset = collision[0].rect.x - self.rect.x
	# 			y_offset = collision[0].rect.y - self.rect.y
	# 			dx = self.mask.overlap_area(collision[0].mask, (x_offset + 1, y_offset)) - self.mask.overlap_area(collision[0].mask, (x_offset - 1, y_offset))
	# 			dy = self.mask.overlap_area(collision[0].mask, (x_offset, y_offset + 1)) - self.mask.overlap_area(collision[0].mask, (x_offset, y_offset - 1))
	# 			overlap_vec += d_p.normalize()
	# 			print(dx,dy)
	# 		self.vel += 1.5*self.vel.magnitude()*overlap_vec.normalize()
	# 		print(self.vel)
	# 	self.pos += self.vel*dt
	# 	self.rect.center = self.pos

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