import pygame

import constants


class World(object):
    def __init__(self, data):
        self.tile_list = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(pygame.image.load(constants.IMG_WOOD_PLATFORM_LEFT), (constants.TILE_SIZE, constants.TILE_SIZE))
                    #img = pygame.Rect((0,0), (constants.TILE_SIZE, constants.TILE_SIZE))
                    img_Rect = img.get_rect()
                    img_Rect.x = col_count * constants.TILE_SIZE
                    img_Rect.y = row_count * constants.TILE_SIZE
                    tile = (img, img_Rect)
                    self.tile_list.append(tile)
                elif tile == 2:
                    img = pygame.transform.scale(pygame.image.load(constants.IMG_WOOD_PLATFORM_CENTER), (constants.TILE_SIZE, constants.TILE_SIZE))
                    img_Rect = img.get_rect()
                    img_Rect.x = col_count * constants.TILE_SIZE
                    img_Rect.y = row_count * constants.TILE_SIZE
                    tile = (img, img_Rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    img = pygame.transform.scale(pygame.image.load(constants.IMG_WOOD_PLATFORM_RIGHT),
                                                 (constants.TILE_SIZE, constants.TILE_SIZE))
                    img_Rect = img.get_rect()
                    img_Rect.x = col_count * constants.TILE_SIZE
                    img_Rect.y = row_count * constants.TILE_SIZE
                    tile = (img, img_Rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self, win):
        for tile in self.tile_list:
            win.blit(tile[0], tile[1])


