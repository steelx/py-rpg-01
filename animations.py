import time as t
from typing import List

import pygame


class Animation:
    def __init__(self, frames: List[int], spf: int = 8, loop=False):
        self.frames = frames
        self.index = 0
        self.fps_rate = spf-1
        self.last_frame_time = pygame.time.get_ticks()
        self.loop = loop

    def update(self, fps):
        print(f"FPS: {fps} index {self.index}")
        current = pygame.time.get_ticks()
        if current > self.last_frame_time and self.fps_rate == fps:
            self.index += 1
            self.last_frame_time = current

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
        return self.is_last_frame()
