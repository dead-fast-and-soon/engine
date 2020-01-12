
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from konkyo.objects.component import BatchComponent
from konkyo.components.sprite import Sprite
from konkyo.structs.vector import Vector

if TYPE_CHECKING:
    from konkyo.asset.image import ImageAsset


@dataclass
class AnimationFrame:
    """
    A class describing a frame of an animation.

    Args:
        image (ImageAsset): the image to display
        duration (float): the amount of time to display this image for
            (in seconds)
        flip_x (bool): if true, flip this image horizontally
        flip_y (bool): if true, flip this image vertically
    """
    image: ImageAsset
    duration: float
    flip_x: bool = False
    flip_y: bool = False
    offset: Vector = Vector(0, 0)


class AnimatedSprite(BatchComponent):

    def on_spawn(self, frames: List[AnimationFrame], layer: int = 0,
                 color: tuple = (255, 255, 255), palette=None,
                 anchor: tuple = None):
        """
        An animated sprite.

        Args:
            frames (List[ImageAsset]): a List of frames to use in this
                                       animation
            frame_duration (float): the duration of each frame of the
                                    animation
        """
        self._raw_frames = frames
        self.frames = [AnimationFrame(*tup) for tup in self._raw_frames]

        # configure Sprite to display first frame
        self.sprite = self.create_component(Sprite, self.position,
                                            self.frames[0].image,
                                            layer=layer,
                                            color=color,
                                            palette=palette,
                                            anchor=anchor)
        # timer to time each frame
        self._timer = 0
        self.is_playing = True

        # the current frame to display
        self.cur_frame_idx = 0
        self.cur_frame_duration = 0

        self.restart()

    @property
    def current_frame(self) -> AnimationFrame:

        return self.frames[self.cur_frame_idx]

    def set_animation(self, frames: List[AnimationFrame]):

        if frames is not self._raw_frames:
            self._raw_frames = frames
            self.frames = [AnimationFrame(*tup) for tup in self._raw_frames]
            self.restart()

    def restart(self, starting_frame: int = 0):
        """
        Start the animation from the first frame.
        """
        self._timer = 0
        self.set_frame(starting_frame % len(self.frames))

    def play(self) -> None:
        """
        Start the animation.
        """
        self.is_playing = True

    def stop(self) -> None:
        """
        Stop the animation.
        """
        self.is_playing = False

    def set_frame(self, idx: int) -> None:
        """
        Configure our sprite to display the given frame.
        """
        frame = self.frames[idx]
        self.cur_frame_idx = idx
        self.cur_frame_duration = frame.duration

        self.sprite.image = self.current_frame.image
        self.sprite.flip_x(self.current_frame.flip_x)
        self.sprite.flip_y(self.current_frame.flip_y)
        self.sprite.position = self.position + self.current_frame.offset

    def get_next_frame_idx(self) -> ImageAsset:
        """
        Return the next frame in the animation.

        Returns:
            ImageAsset: the next frame in the animation
        """
        next_frame_idx = (self.cur_frame_idx + 1) % len(self.frames)
        return next_frame_idx

    def on_update(self, delta: float):

        self._timer += delta

        while self._timer >= self.cur_frame_duration:
            self._timer -= self.cur_frame_duration
            next_frame_idx = self.get_next_frame_idx()
            self.set_frame(next_frame_idx)

    def on_set_visible(self):
        self.sprite.is_visible = True

    def on_set_hidden(self):
        self.sprite.is_visible = False
