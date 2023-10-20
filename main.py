import os
import pygame
import sys
from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game

PATH = os.path.abspath('.') + '/assets/'


def load_sprite_sheet(sprite_sheet_path: str, frame_width: int, frame_height: int, rows: int, columns: int):
    # Load the sprite sheet
    sprite_sheet = pygame.image.load(sprite_sheet_path)

    # Calculate the total number of frames
    total_frames = rows * columns

    # Create a list of frames
    frames = []

    # Split the sprite sheet into frames
    for row in range(rows):
        for col in range(columns):
            frame = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            frames.append(sprite_sheet.subsurface(frame))

    return frames


if __name__ == '__main__':
    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption("jRPG Game")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        cave_map = Game(PATH + 'small_room.tmx')

        cave_map.setup()
        cave_map.go_to_tile(6, 5)

        hero_height = 24
        hero_width = 16
        hero_sprites = load_sprite_sheet(PATH + 'walk_cycle.png', hero_width, hero_height, 9, 16)
        hero_pos = cave_map.get_tile_foot(10, 2, 4)
        print(f"without modifier: {cave_map.get_tile_foot(10, 2)}")
        print(f"with modifier: {cave_map.get_tile_foot(10, 2, 4)}")
        hero = pygame.sprite.Sprite(cave_map.map_group)
        hero.image = hero_sprites[8]
        hero.rect = hero.image.get_rect(center=hero_pos)


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Input
            # Handle user input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                cave_map.cam_x -= 5
            if keys[pygame.K_RIGHT]:
                cave_map.cam_x += 5
            if keys[pygame.K_UP]:
                cave_map.cam_y -= 5
            if keys[pygame.K_DOWN]:
                cave_map.cam_y += 5

            # Game Render
            cave_map.render()
            cave_map.update()

            # get tile position
            # mouse_x, mouse_y = pygame.mouse.get_pos()
            # tile_x, tile_y = cave_map.point_to_tile(mouse_x, mouse_y)
            # print(f"Tile {tile_x}, {tile_y}")

            pygame.display.update()
            clock.tick(60)
