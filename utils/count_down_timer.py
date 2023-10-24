import pygame


class CountdownTimer:
    def __init__(self, duration: float):
        self.start_time = pygame.time.get_ticks()
        self.duration = duration * 1000  # Convert seconds to milliseconds

    def has_elapsed(self) -> bool:
        current_time = pygame.time.get_ticks()
        return (current_time - self.start_time) >= self.duration

    def reset(self, duration: float = None):
        if duration:
            self.duration = duration * 1000
        self.start_time = pygame.time.get_ticks()
