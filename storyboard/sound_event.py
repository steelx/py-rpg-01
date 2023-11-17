import pygame


class SoundEvent:
    def __init__(self, sound_file: str, volume=1.0):
        self.sound = pygame.mixer.Sound(sound_file)
        self.sound.set_volume(volume)
        self.played = False

    def stop(self):
        self.sound.fadeout(500)

    def update(self, dt):
        if not self.played:
            self.sound.play(fade_ms=500)
            self.played = True

    def is_blocking(self) -> bool:
        return False  # This event is not blocking

    def is_finished(self) -> bool:
        return not pygame.mixer.get_busy()  # Check if any sounds are still playing
