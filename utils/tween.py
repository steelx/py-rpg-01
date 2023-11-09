class TweenTo:
    def __init__(self, start: float, finish: float, duration: float):
        """
        :param start: starting value
        :param finish: ending value
        :param duration: time to reach from start to finish in seconds
        """
        self.start = start
        self.finish = finish
        self.duration = duration * 1000.0  # Convert to milliseconds
        self.elapsed = 0.0  # Time elapsed since the start of the tween
        self.value = start  # Current value of the tween

    def update(self, dt: float):
        """
        Update the tween value based on the delta time.

        :param dt: time since last update in seconds
        """
        if self.elapsed < self.duration:
            self.elapsed += dt
            # Calculate the interpolation factor (percentage of completion)
            t = min(self.elapsed / self.duration, 1)
            # Update the current value by linear interpolation
            self.value = self.start + t * (self.finish - self.start)
        else:
            # Ensure the final value is set accurately
            self.value = self.finish

    def is_finished(self) -> bool:
        """
        Check if the tweening has finished.

        :return: True if the tweening is finished, False otherwise
        """
        return self.elapsed >= self.duration
