from globals import DISPLAY_SIZE


class Camera:
    def __init__(self, game, width_pixel, height_pixel):
        self.game = game
        self.cam_x = 0
        self.cam_y = 0
        self.width_pixel = width_pixel
        self.height_pixel = height_pixel
        self.follow = None

    def get_position(self):
        return self.cam_x, self.cam_y

    def follow_entity(self):
        target_x, target_y = self.follow.rect.center
        self.go_to(target_x, target_y)

    def go_to(self, x: int, y: int):
        self.cam_x = x - DISPLAY_SIZE[0] // 2
        self.cam_y = y - DISPLAY_SIZE[1] // 2
        self._clamp_camera()

    def _clamp_camera(self):
        # Ensure the camera doesn't move beyond the map edges
        self.cam_x = max(self.cam_x, 0)
        self.cam_y = max(self.cam_y, 0)
        self.cam_x = min(self.cam_x, self.width_pixel - DISPLAY_SIZE[0])
        self.cam_y = min(self.cam_y, self.height_pixel - DISPLAY_SIZE[1])
