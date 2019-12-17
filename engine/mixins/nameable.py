

class Nameable:
    """
    An object that can be given a custom name.
    """
    def __init__(self, *args, name: str = None, **kwargs):
        super().__init__(*args, **kwargs)  # type: ignore

        if name is None:
            name = type(self).__name__

        self.name = name
