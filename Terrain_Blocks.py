import pygame
from pygame import display
from pygame.math import Vector2
import math

class block(pygame.sprite.Sprite):
	def __init__(self, pos, desc, sheet, ppos, size, parent, group): # contains a surface 'block'
		super().__init__(group)
		##  the rect that defines the shape
		self.desc = desc
		self.pos = Vector2()
		self.pos.update(pos)
		self.nrect = pygame.Rect(pos, (25, 25))
		self.image_b = pygame.Surface(self.nrect.size,pygame.SRCALPHA)
		
		self.rect = pygame.Rect(ppos[0],ppos[1]+300,size[0],size[1])
		self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		
		self.image_b.blit(sheet, (0,0), self.nrect)

		pygame.transform.scale(self.image_b, size, self.image)
		self.mask = pygame.mask.from_surface(self.image)

		parent.blit(self.image, self.rect)
		

	def update(self, screen):
		screen.blit(self.image,self.rect)
		self.mask = pygame.mask.from_surface(self.image)

	# returns the overlap offsets
	def overlap(self, node_rect):
		overlap_vec = Vector2()
		x_offset = self.rect.x - node_rect.rect.x
		y_offset = self.rect.y - node_rect.rect.y
		dx = node_rect.mask.overlap_area(self.mask, (x_offset + 1, y_offset)) - node_rect.mask.overlap_area(self.mask, (x_offset - 1, y_offset))
		dy = -(node_rect.mask.overlap_area(self.mask, (x_offset, y_offset + 1)) - node_rect.mask.overlap_area(self.mask, (x_offset, y_offset - 1)))
		while dx != 0 or dy != 0:
			d_p = Vector2(dx,dy)
			node_rect.pos += d_p.normalize()
			node_rect.rect.center = node_rect.pos
			x_offset = self.rect.x - node_rect.rect.x
			y_offset = self.rect.y - node_rect.rect.y
			dx = node_rect.mask.overlap_area(self.mask, (x_offset + 1, y_offset)) - node_rect.mask.overlap_area(self.mask, (x_offset - 1, y_offset))
			dy = node_rect.mask.overlap_area(self.mask, (x_offset, y_offset + 1)) - node_rect.mask.overlap_area(self.mask, (x_offset, y_offset - 1))
			overlap_vec += d_p.normalize()
		node_rect.vel += 1.125*node_rect.vel.magnitude()*overlap_vec.normalize()


class terrain():
	def __init__(self, width, height): 
		self.terrain_sheet = pygame.image.load("Terrain_3.png").convert_alpha()
		self.terrain_list = pygame.sprite.Group()

		# Need to create a dictionary that holds all of the terrain blocks 
		self.terrain_dict = {'LRC': (0,0)}
		self.terrain_dict['LLC'] = (25,0)
		self.terrain_dict['URC'] = (50,0)
		self.terrain_dict['ULC'] = (75,0)
		self.terrain_dict['LSF'] = (100,0)
		self.terrain_dict['RSF'] = (125,0)
		self.terrain_dict['BSF'] = (0,25)
		self.terrain_dict['LRF'] = (25,25)
		self.terrain_dict['LLF'] = (50,25)
		self.terrain_dict['URF'] = (75,25)
		self.terrain_dict['ULF'] = (100,25)
		self.terrain_dict['BTM'] = (125,25)


	def set_terrain(self, terr_outline, surface):
		# terr_outline is a dict of UL corner coords with the text indicator for the block at that coord
		for terr, pos in terr_outline :
			block(self.terrain_dict[terr], terr, self.terrain_sheet, pos, (50,50), surface, self.terrain_list)
			for y in range(pos[1]+50,surface.get_height()-301,50):
				if not terr in ['LRC','URC','LSF','RSF']:
					block(self.terrain_dict['BTM'], 'BTM', self.terrain_sheet, (pos[0],y), (50,50), surface, self.terrain_list)

	def render_terrain(self,screen):
		self.terrain_list.update(screen)

		