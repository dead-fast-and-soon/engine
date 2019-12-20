
from __future__ import annotations

import typing as t

from engine.objects.component import BatchComponent
from engine.components.sprite import Sprite

if t.TYPE_CHECKING:
    from engine.asset.image import ImageAsset


class AnimatedSprite(BatchComponent):

    def on_spawn(self, frames: t.List[ImageAsset], frame_duration: float):
        """
        An animated sprite.

        Args:
            frames (t.List[ImageAsset]): a t.List of frames to use in this
                                       animation
            frame_duration (float): the duration of each frame of the
                                    animation
        """
        self.frames = frames
        self.sprite = self.create_component(Sprite, self.position,
                                            self.frames[0])
        self.sprite.offset = (-8, -8)  # center image
        self.frame_duration = frame_duration
        self._timer = 0

        self.current_frame = 0

    def next_frame(self) -> ImageAsset:
        """
        Return the next frame in the animation.

        Returns:
            ImageAsset: the next frame in the animation
        """
        next_frame = self.current_frame + 1
        if next_frame >= len(self.frames):
            next_frame = 0
            self.sprite.flip_x()
        self.current_frame = next_frame
        return self.frames[next_frame]

    def on_update(self, delta: float):

        self._timer += delta

        while self._timer >= self.frame_duration:
            self.sprite.image = self.next_frame()
            self._timer -= self.frame_duration

    def on_set_visible(self):
        self.sprite.is_visible = True

    def on_set_hidden(self):
        self.sprite.is_visible = False
