
from collections import namedtuple
from typing import List, Any


class StateSection(namedtuple('StateSection', ['length', 'value'])):
    """
    Determines what `StateTimer.current_state` will be during the specified
    amount of time `length`.
    """
    pass


class FrameData:

    NOT_ACTIVE = -1

    def __init__(self, sections: List[tuple]):
        """
        FrameData contains a timer that returns a specific state
        depending on how long the timer has been running.

        Args:
            sections (List[StateSection]): a list of sections in this data
        """
        # sections
        self.sections: List[StateSection] = [StateSection(*tup)
                                             for tup in sections]
        # the current section to look at;
        # -1 means this framedata isn't active
        self.section_index: int = -1

        # the timer to use to time each section
        self.timer: float = 0

    @property
    def is_active(self) -> bool:
        """
        Return True if this timer is active.

        Returns:
            [type]: [description]
        """
        return self.section_index != -1

    @property
    def current_section(self) -> StateSection:
        return self.sections[self.section_index]

    @property
    def current_state(self) -> Any:
        """
        Return the appropriate value depending on the active section

        Returns:
            [type]: [description]
        """
        if self.section_index == -1:
            return FrameData.NOT_ACTIVE
        else:
            return self.current_section.value

    def update(self, delta: float) -> None:
        """
        Update the timer, indicating that a frame has passed.

        Args:
            delta (float): the time difference since the last frame
        """
        if self.is_active:

            self.timer += delta

            if self.timer >= self.current_section.length:

                if self.section_index == (len(self.sections) - 1):
                    self._set_section(-1)
                else:
                    self._set_section(self.section_index + 1)

    def section_progress(self, i: int) -> float:
        """
        Get how much time has passed for the specified section `i`,
        in percent.

        Returns:
            float: a percent of the elapsed time for the current section
        """
        if not self.is_active or self.section_index > i:
            # if request index is less than the current, always return 1
            return 1

        if self.section_index < i:
            # if request index is greater than the current, always return 0
            return 0

        return self.timer / self.current_section.length

    def _set_section(self, i: int):
        self.section_index = i
        self.timer = 0

    def start(self) -> None:
        self._set_section(0)
