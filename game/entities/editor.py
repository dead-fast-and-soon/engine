
import traceback
from dataclasses import dataclass

from pyglet.window import key

from konkyo.asset.image import ImageAsset
from konkyo.asset.managers.tileset import TilesetManager
from konkyo.asset.tileset import TilesetAsset
from konkyo.components.shapes import Box2D
from konkyo.components.sprite import Sprite
from konkyo.objects.entity import Entity
from game.components.tile import TileSprite, TileSpriteFactory
from game.structs.tilemeta import TileMeta
from konkyo.structs.vector import Vector


@dataclass
class WorldTile:
    idx: int = -1  # the index of the tile
    sprite: Sprite = None  # the sprite, or none if part of a region
    size: tuple = None  # the size of the region, none if part of a region
    parent: Vector = None  # the parent tile if part of a region


NO_TILE = WorldTile()
NO_PREFAB = (-1, None)

prefabs = [
    TileMeta('grass', 'kanto', (44, 44, 44, 44), (155, 255, 65)),
    TileMeta('path', 'kanto', (57, 57, 57, 57)),
    TileMeta('bush', 'kanto', (64, 65, 80, 81), (0, 255, 0), True),
    TileMeta('sign', 'kanto', (70, 71, 86, 87), (255, 255, 255), True)
]


class Editor(Entity):

    MODE_TILE = 0  # switch each 8x8 image manually
    MODE_PREFAB = 1  # switch 16x16 tile between premade tiles

    def on_spawn(self):

        print('loading tilesets... ')

        self._tilesets = {
            'kanto': TilesetAsset('assets/kanto.png', 8),
            # 'tileset': TilesetAsset('assets/tileset.png', 16)
        }

        self.tset8 = self._tilesets.get('kanto')

        print('creating marker... ')
        self.marker = self.create_component(Box2D, (-8, -16), (16, 16),
                                            color=(0, 255, 0),
                                            is_filled=False,
                                            layer=1)

        self._mode = Editor.MODE_TILE

        self.grid_pos = Vector(0, 0)
        self.grid_size = 8

        self._region_w = 1
        self._region_h = 1

        self.tilemap = dict()
        self.prefabmap = dict()

        self.is_16 = True
        self._wireframe = False

        self._keys = self.scene.game.input

        print('updating marker... ')
        self.update_marker()

        print('editor created')

    def _get_tile_image(self, i: int):

        i = i % self.tset8.length
        return self.tset8.get_tile(i)

    def _get_prefab_tile(self, i: int):

        print('getting {}'.format(i))
        i = i % len(prefabs)
        return prefabs[i]

    def _get_prefab_at(self, grid_pos: Vector):
        return self.prefabmap.get(tuple(grid_pos), NO_PREFAB)

    def _set_prefab_to(self, grid_pos: Vector, val):
        self.prefabmap[tuple(grid_pos)] = val

    def _del_prefab_at(self, grid_pos: Vector):
        del self.prefabmap[tuple(grid_pos)]

    def _add_sprite(self, grid_pos: Vector, image):

        pos = self.grid_to_world(grid_pos)
        return self.create_component(Sprite, pos, image, layer=0)

    def set_tile_to(self, grid_pos: Vector, i: int):

        key = tuple(grid_pos)
        image = self._get_tile_image(i)

        if key not in self.tilemap:
            sprite = self._add_sprite(grid_pos, image)
            sprite.set_scale(2)
            sprite.set_tex_coords((0, 2), (0, 2))

        else:
            sprite = self.tilemap[key].sprite
            sprite.image = image

        self.tilemap[key] = WorldTile(i, sprite, None)

    def clear_tile(self, grid_pos: Vector):

        tile = self.get_tile(grid_pos)

        if tile is not NO_TILE:
            del self.tilemap[tuple(grid_pos)]
            print('  clearing tile ({}, {}) size: ({}, {})'
                  .format(*grid_pos, *tile.size))
            # print(self.vertex_list.domain.allocator.starts)
            self.scene.destroy_component(tile.sprite)

    def clear_prefab(self, grid_pos: Vector):

        prefab = self._get_prefab_at(grid_pos)

        if prefab is not NO_PREFAB:
            self._del_prefab_at(grid_pos)
            print('  clearing prf @ ({}, {})'.format(*grid_pos))
            # print(self.vertex_list.domain.allocator.starts)
            self.scene.destroy_component(prefab[1])

    def change_mode(self):

        if self._mode is Editor.MODE_TILE:
            self._mode = Editor.MODE_PREFAB

            self.grid_size = 16
            self.grid_pos = self.grid_pos // 2
            self.marker.color = (255, 0, 0)

        else:
            self._mode = Editor.MODE_TILE

            self.grid_size = 8
            self.grid_pos = self.grid_pos * 2
            self.marker.color = (0, 255, 0)

        self.update_marker()

    def set_tile_region(self, grid_pos: Vector, i: int):

        key = tuple(grid_pos)
        w, h = (self._region_w * (self.grid_size // 8),
                self._region_h * (self.grid_size // 8))  # grid size of region
        image = self._get_tile_image(i)

        # ensure all these tiles are empty
        print('setting ({}, {}) size: ({}, {})'
              .format(grid_pos.x, grid_pos.y,
                      self._region_w, self._region_h))
        for x in range(grid_pos.x, grid_pos.x + self._region_w):
            for y in range(grid_pos.y, grid_pos.y + self._region_h):
                self.clear_tile(Vector(x, y))

        if key not in self.tilemap:
            sprite = self._add_sprite(grid_pos, image)
            sprite.set_scale_x(w)
            sprite.set_scale_y(h)
            sprite.set_tex_coords((0, w), (0, h))

        else:
            sprite = self.tilemap[key].sprite
            sprite.image = image

        self.tilemap[key] = WorldTile(i, sprite, (w, h), None)
        if self._wireframe:
            sprite.toggle_wireframe()

    def set_prefab_region(self, grid_pos: Vector, i: int):

        # TODO: support regions
        p_tile = self._get_prefab_tile(i)

        print('setting ({}, {}) to {}'.format(*grid_pos, p_tile.name))
        self.clear_prefab(grid_pos)

        sprite = self._factory.create_tile(p_tile,
                                           self.grid_to_world(grid_pos))
        self._set_prefab_to(grid_pos, (i, sprite))

    def get_tile(self, grid_pos: Vector) -> WorldTile:

        key = tuple(grid_pos)
        if key in self.tilemap:
            return self.tilemap[key]
        else:
            return NO_TILE

    def next_tile(self):

        if self._mode is Editor.MODE_TILE:
            cur_tile_idx = self.get_tile(self.grid_pos).idx
            self.set_tile_region(self.grid_pos, cur_tile_idx + 1)
        else:
            cur_idx = self._get_prefab_at(self.grid_pos)[0]
            print(f'cur_idx { cur_idx }')
            self.set_prefab_region(self.grid_pos, cur_idx + 1)

    def prev_tile(self):

        if self._mode is Editor.MODE_TILE:
            cur_tile_idx = self.get_tile(self.grid_pos).idx
            self.set_tile_region(self.grid_pos, cur_tile_idx - 1)
        else:
            cur_idx = self._get_prefab_at(self.grid_pos)[0]
            self.set_prefab_region(self.grid_pos, cur_idx - 1)

    def toggle_wireframe(self):
        self._wireframe = not self._wireframe
        for i, tile in self.tilemap.items():
            if tile.sprite:
                tile.sprite.toggle_wireframe()
        for i, tile in self.prefabmap.items():
            if tile[1]:
                for sprite in tile[1]._sprites:
                    sprite.toggle_wireframe()

    def on_key_press(self, symbol, modifiers):

        # movement
        if symbol in [key.W, key.S, key.A, key.D]:
            if symbol is key.W:
                adj = (0, 1)
            if symbol is key.S:
                adj = (0, -1)
            if symbol is key.D:
                adj = (1, 0)
            if symbol is key.A:
                adj = (-1, 0)

            cur_idx = self._get_prefab_at(self.grid_pos)[0]
            self.grid_pos += adj
            self.update_marker()

            # copy tile from last position
            if modifiers & key.MOD_SHIFT:
                self.set_prefab_region(self.grid_pos, cur_idx)

        # region sizing
        if symbol in [key.I, key.J, key.K, key.L]:
            if symbol is key.I:
                self._region_h += 1
            if symbol is key.K:
                self._region_h -= 1
            if symbol is key.L:
                self._region_w += 1
            if symbol is key.J:
                self._region_w -= 1
            self.update_marker()

        # tile switching
        if symbol in [key.Q, key.E]:
            # 1 or 10
            times = 1 + (modifiers & key.MOD_SHIFT) * 9

            if symbol is key.E:
                fn = self.next_tile
            else:
                fn = self.prev_tile

            for _ in range(times):
                fn()

        # size toggle
        if symbol is key.SPACE:
            self.change_mode()

        if symbol is key.Z:
            self.toggle_wireframe()

    def grid_to_world(self, grid_pos: Vector) -> Vector:

        return self.grid_pos * self.grid_size - (16, 8)

    def update_marker(self):

        self.marker.position = self.grid_to_world(self.grid_pos)
        self.marker.size = (self.grid_size * self._region_w,
                            self.grid_size * self._region_h)

    def on_key_release(self, key, mod):
        pass

    @Entity.limit_rate(10)
    def on_update(self, delta: float):

        self.console_set(2, 'pos: {}'.format(self.grid_pos))
        self.console_set(3, 'tile: {} / {}'.format(
            self.get_tile(self.grid_pos).idx,
            self.tset8.length - 1))
        self.console_set(4, 'region: ({}, {})'
                         .format(self._region_w, self._region_h))
        self.console_set(5, 'comps: {}'.format(
            self.scene.component_count))
