import pygame


def load_sprite_sheet(sprite_sheet_path: str, frame_width: int, frame_height: int, rows: int, columns: int):
    # Load the sprite sheet
    sprite_sheet = pygame.image.load(sprite_sheet_path)
    # Create a list of frames
    frames = []
    # Split the sprite sheet into frames
    for row in range(rows):
        for col in range(columns):
            frame = pygame.Rect(col * frame_width, row *
                                frame_height, frame_width, frame_height)
            frames.append(sprite_sheet.subsurface(frame))

    return frames
