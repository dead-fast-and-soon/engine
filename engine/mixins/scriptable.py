
from typing import Callable


class Scriptable:
    """
    An object that can be updated per tick.
    """
    def __init__(self, *args, **kwargs):
        super(Scriptable, self).__init__(*args, **kwargs)

    def update(self, delta: float):
        """
        Update this object.

        Args:
            delta (float): time elapsed since the last tick.
        """

    def on_update(self, delta: float):
        """
        Called every tick.

        Args:
            delta (float): time elapsed since the last tick.
        """
        pass

    @staticmethod
    def limit_rate(rate: float) -> Callable:
        """
        Modify an `on_update()` function to only call at a fixed rate.

        Args:
            update_fn (Callable): [description]

        Returns:
            Callable: the new function
        """
        assert rate > 0, 'rate must be higher than 0'
        seconds_per_tick = 1 / rate

        def decorator(update_fn: Callable) -> Callable:
            def new_update_fn(self, delta: float):
                if not hasattr(self, '_accum_time'):
                    self._accum_time = 0

                self._accum_time += delta
                if self._accum_time > seconds_per_tick:
                    update_fn(self, seconds_per_tick)
                    while self._accum_time > seconds_per_tick:
                        self._accum_time -= seconds_per_tick

            return new_update_fn
        return decorator
