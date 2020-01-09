
from konkyo.asset.tileset import TilesetAsset


class TilesetManager:
    """
    Stores multiple tilesets for easy access and to minimize
    loading the same tileset multiple times.
    """
    def __init__(self):
        self._tilesets = dict()

    def _get_path(self, name: str):
        return 'assets/{}.png'.format(name)

    def load(self, name: str, size: int):
        """
        Load a tileset.

        Args:
            name (str): the name of the tileset
            size (int): the width and height of each tile
        """
        if name not in self._tilesets:
            self._tilesets[name] = TilesetAsset(self._get_path(name), size)

    def get(self, name: str) -> TilesetAsset:
        """
        Return a tileset, loading it if it wasn't already.

        Args:
            name (str): the name of the tileset
        """
        return self._tilesets[name]
