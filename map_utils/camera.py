from globals import DISPLAY_SIZE


class Camera:
    def __init__(self, game, width_pixel, height_pixel):
        self.game = game
        self.x = 0
        self.y = 0
        self.width_pixel = width_pixel
        self.height_pixel = height_pixel
        self.follow = None

    def get_position(self):
        return self.x, self.y

    def follow_entity(self):
        target_x, target_y = self.follow.rect.center
        self.go_to(target_x, target_y)

    def go_to(self, x: int, y: int):
        self.x = x - DISPLAY_SIZE[0] // 2
        self.y = y - DISPLAY_SIZE[1] // 2
        self._clamp_camera()

    def _clamp_camera(self):
        # Ensure the camera doesn't move beyond the map edges
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)
        self.x = min(self.x, self.width_pixel - DISPLAY_SIZE[0])
        self.y = min(self.y, self.height_pixel - DISPLAY_SIZE[1])
