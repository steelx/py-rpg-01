from typing import List

import pygame


class Animation:
    def __init__(self, frames: List[int], ms: int = 100, loop=False):
        """
        :param frames: animation frames
        :param ms: gap between next frame in milliseconds higher number means slower animation
        :param loop: run animation in loop
        """
        self.frames = frames
        self.index = 0
        self.ms = ms
        self.loop = loop
        self.next_frame_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() > self.next_frame_time:
            self.next_frame_time += self.ms
            self.index = (self.index + 1) % len(self.frames)

            if self.is_last_frame():
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames) - 1

    def set_frames(self, frames):
        self.frames = frames
        self.index = 0

    def frame(self):
        return self.frames[self.index]

    def get_first_frame(self):
        return self.frames[0]

    def is_last_frame(self) -> bool:
        return True if self.index >= len(self.frames) - 1 else False

    def is_finished(self):
        return self.is_last_frame() or not self.loop
