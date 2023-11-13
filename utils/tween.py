from typing import Any

import pygame


def easeInOutQuad(t: float) -> float:
    """
    Easing function that accelerates and then decelerates the transition.

    :param t: A float representing the current time normalized between 0 and 1 (start and end of the transition).
    :return: The adjusted value at time t.
    """
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t


class TweenTo:
    def __init__(self, container: Any, key: str, finish: float, duration: float):
        """
        :param finish: ending value
        :param duration: time to reach from start to finish in seconds
        """
        if isinstance(container, pygame.Color) and key == "a":
            self.start_value = container.a  # Accessing the alpha value directly
        else:
            assert hasattr(container, key), f"{container} does not have attribute {key}"
            self.start_value = getattr(container, key)
        self.key = key
        self.duration = duration * 1000.0  # Convert to milliseconds
        self.elapsed = 0.0
        self._container = container  # Object to tween
        self.end_value = finish
        self.easing_function = easeInOutQuad

    def _calculate_tween_value(self, dt: float) -> float:
        """ Calculate the current tween value based on delta time. """
        self.elapsed += dt
        normalized_time = min(1.0, self.elapsed / self.duration)
        eased_time = self.easing_function(normalized_time)
        return self.start_value + (self.end_value - self.start_value) * eased_time

    def _update_attribute(self, value: float):
        """ Update the attribute of the object based on the tween value. """
        if isinstance(self._container, pygame.Color) and self.key == "a":
            setattr(self._container, self.key, int(value))  # For Color, ensure integer and use 'a' for alpha
        else:
            setattr(self._container, self.key, value)  # Generic case

    def update(self, dt: float):
        """
        Update the tween value based on the delta time.
        :param dt: time since last update in seconds
        """
        if self.elapsed < self.duration:
            tween_value = self._calculate_tween_value(dt)
            self._update_attribute(tween_value)
        else:
            # Ensure the final value is set accurately
            self._update_attribute(self.end_value)

    def is_finished(self) -> bool:
        """
        Check if the tweening has finished.

        :return: True if the tweening is finished, False otherwise
        """
        return self.elapsed >= self.duration
