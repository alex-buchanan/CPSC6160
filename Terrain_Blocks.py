import pygame
from pygame import display
import math

class block():
	def __init__(self, pos, sheet, ppos, size, parent): # contains a surface 'block'
		##  the rect that defines the shape
		x = pos[0]
		y = pos[1]
		self.block = pygame.Rect(x, y, 25, 25)
		self.image = pygame.Surface(self.block.size)
		# print("surface(x,y) = ("+str(ppos[0])+","+str(ppos[1]+300)+")")
		self.block_s = pygame.Rect(ppos[0],ppos[1]+300,size[0],size[1])
		self.image_s = parent.subsurface(self.block_s)
		self.image_s.set_colorkey((255,255,255))
		# self.image.set_colorkey([255,255,255])
		self.image.blit(sheet, (0,0), self.block)
		pygame.transform.scale(self.image, size, self.image_s)
		self.mask = pygame.mask.from_surface(self.image_s)

class terrain():
	def __init__(self, width, height): 
		self.terrain_sheet = pygame.image.load("Terrain_2.png")
		# self.terrain_sheet.set_colorkey((0,0,0))
		self.terrain_list = []
		self.floor_rect = pygame.Rect(0, 0, width, height)
		self.floor_surface = pygame.Surface(self.floor_rect.size, pygame.SRCALPHA)	
		# self.floor_surface.set_colorkey([255,255,255])
		self.terr_mask = None

		# Need to create a dictionary that holds all of the terrain blocks 
		self.terrain_dict = {'LRC': (0,0)}
		self.terrain_dict['LLC'] = (25,0)
		self.terrain_dict['URC'] = (50,0)
		self.terrain_dict['ULC'] = (75,0)
		self.terrain_dict['LLF'] = (100,0)
		self.terrain_dict['LRF'] = (125,0)
		self.terrain_dict['URF'] = (150,0)
		self.terrain_dict['ULF'] = (175,0)
		self.terrain_dict['LSF'] = (0,25)
		self.terrain_dict['RSF'] = (25,25)
		self.terrain_dict['BSF'] = (50,25)
		self.terrain_dict['TSF'] = (75,25)
		self.terrain_dict['BTM'] = (100,25)


	def set_terrain(self, terr_outline, surface):
		# terr_outline is a dict of UL corner coords with the text indicator for the block at that coord
		for terr, pos in terr_outline :
			self.terrain_list.append(block(self.terrain_dict[terr], self.terrain_sheet, pos, (100,100), surface))
			for y in range(pos[1]+100,surface.get_height()-301,50):
				self.terrain_list.append(block(self.terrain_dict['BTM'], self.terrain_sheet, (pos[0],y), (100,50), surface))

	def get_terrain(self):
		return self.floor_surface

		