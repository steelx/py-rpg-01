import time as t
from typing import List

import pygame


class Animation:
    def __init__(self, frames: List[int], spf: int = 0.08, loop=False):
        self.frames = frames
        self.index = 0
        self.spf = spf*1000
        self.loop = loop
        self.next_frame = pygame.time.get_ticks()

    def update(self):
        print(f"Frame no {self.index}")
        if pygame.time.get_ticks() > self.next_frame:
            self.next_frame += self.spf
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
