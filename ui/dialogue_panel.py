# dialogue_panel.py
from typing import Tuple
import pygame
import pygame_gui
from globals import WINDOW_SIZE
from ui import Panel

AVATAR_WIDTH_RATIO = 0.15

class DialoguePanel(Panel):
    def __init__(self, manager: pygame_gui.UIManager, window_size: Tuple[int, int] = WINDOW_SIZE, **kwargs):
        bottom_panel_height = int(0.30 * window_size[1])
        super().__init__(0, window_size[1] - bottom_panel_height, window_size[0], bottom_panel_height, manager,
                         **kwargs)

    def setup_dialogue(self, hero_image: str, hero_name: str, message: str):
        self.add_image(hero_image)
        self.add_title_and_message(hero_name, message)

    def add_image(self, image_path: str, pos: Tuple[int, int] = (5, 5)):
        avatar_size = (self.rect.width * AVATAR_WIDTH_RATIO, self.rect.height * 0.75)
        image_surface = pygame.image.load(image_path).convert_alpha()

        # Preserving aspect ratio while scaling
        aspect_ratio = image_surface.get_width() / image_surface.get_height()
        new_width = avatar_size[0]
        new_height = int(new_width / aspect_ratio)

        if new_height > avatar_size[1]:
            new_height = avatar_size[1]
            new_width = int(new_height * aspect_ratio)

        image_surface = pygame.transform.scale(image_surface, (new_width, new_height))

        avatar = pygame_gui.elements.UIImage(
            pygame.Rect(pos, (new_width, new_height)),
            image_surface,
            manager=self.ui_manager,
            container=self
        )
        return avatar

    def add_title_and_message(self, title: str, message: str, pos: Tuple[int, int] = (125, 5),
                              size: Tuple[int, int] = None):
        size = (self.rect.width * (1 - AVATAR_WIDTH_RATIO), self.rect.height * 0.75) if size is None else size
        size = (size[0] - 50, size[1])

        title_label = pygame_gui.elements.UITextBox(
            title,
            pygame.Rect(pos, size),
            manager=self.ui_manager,
            container=self,
            object_id='@text_title',
            anchors={"left": "left"}
        )
        pos = (pos[0], pos[1] + 30)
        size = (size[0], size[1] + 40)
        text_box = pygame_gui.elements.UITextBox(
            message,
            pygame.Rect(pos, size),
            manager=self.ui_manager,
            container=self,
            object_id='@text_message'
        )

        return title_label, text_box
