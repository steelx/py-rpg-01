import pygame


class CountdownTimer:
    def __init__(self, duration: int):
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def has_elapsed(self) -> bool:
        current_time = pygame.time.get_ticks()
        return (current_time - self.start_time) >= self.duration

    def reset(self, duration: int = None):
        if duration:
            self.duration = duration
        self.start_time = pygame.time.get_ticks()
