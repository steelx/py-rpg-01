import os
import sys

import pygame
import buildtiledmap as tmx

PATH = os.path.abspath('.') + '/assets/'

if __name__ == '__main__':
    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption("jRPG Game")
        screen_width = 320
        screen_height = 240
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()

        font = pygame.font.SysFont('Arial', 12, bold=True)

        tmx_map = tmx.load_tmx_map(PATH + 'cave/cave_map.tmx')

        gTop = (screen_height / 2) - (tmx_map.tileheight * tmx_map.height / 2)
        gLeft = (screen_width / 2) - (tmx_map.tilewidth * tmx_map.width / 2)

        cave_map_group = pygame.sprite.Group()
        debug_group = pygame.sprite.Group()

        tmx.build_tiled_map(tmx_map, cave_map_group, debug_group)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Game Render
            cave_map_group.draw(screen)
            debug_group.draw(screen)

            # get tile position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            tile_x, tile_y = tmx.point_to_tile(mouse_x, mouse_y, tmx_map.tilewidth, tmx_map.width, tmx_map.height)
            mouse_location = f"{tile_x}, {tile_y}"
            img = font.render(
                mouse_location, True, pygame.Color('black'), pygame.Color('white')
            )
            screen.blit(img, (mouse_x+2, mouse_y+20))

            pygame.display.flip()
            clock.tick(60)
