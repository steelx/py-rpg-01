from typing import Dict, List

import pygame

sprite_sheet_cache: Dict[str, List[pygame.Surface]] = {}


def load_sprite_sheet(sprite_sheet_path: str, frame_width: int, frame_height: int, rows: int, columns: int):
    # Check if the sprite sheet is already loaded
    if sprite_sheet_path in sprite_sheet_cache:
        return sprite_sheet_cache[sprite_sheet_path]

    # Load the sprite sheet
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    # Create a list of frames
    frames = []
    # Split the sprite sheet into frames
    for row in range(rows):
        for col in range(columns):
            frame = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            frames.append(sprite_sheet.subsurface(frame))

    # Store the loaded frames in the cache
    sprite_sheet_cache[sprite_sheet_path] = frames
    return frames
