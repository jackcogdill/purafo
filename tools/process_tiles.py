#!/usr/bin/env python3

from PIL import Image, ImageDraw
from collections.abc import Callable
from sys import argv
from typing import TypedDict
import json

TSIZE = 32
CROP_PAD = TSIZE * 2
COLORS = ['red', 'blue', 'green', 'yellow']

Box = tuple[int, int, int, int]  # (left, top, right, bottom)
Point = tuple[int, int]  # (x, y)
WaterTest = Callable[[Point], bool]


class Tile(TypedDict):
  name: str
  color: str
  background: bool
  srcx: int
  srcy: int
  bbox: Box | None


class Islands:

  def __init__(self, w: int, h: int, water_test: WaterTest):
    self.w = w
    self.h = h
    self.is_water = water_test
    self.visited = set()
    self.moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

  def find(self) -> list[Box]:
    islands = []
    for y in range(self.h):
      for x in range(self.w):
        p = (x, y)
        if p in self.visited:
          continue
        if self.is_water(p):
          self.visited.add(p)
          continue
        box = self.__explore_island(p)
        islands.append(box)
        print('Found island %03d size: [%3d x %3d]' %
              (len(islands), *get_size(box)))
    return islands

  def __explore_island(self, start: Point) -> Box:
    land = []
    stack = [start]
    while stack:
      p = stack.pop()  # DFS
      x, y = p
      if x < 0 or x >= self.w or y < 0 or y >= self.h:
        continue
      if p in self.visited:
        continue
      self.visited.add(p)
      if not self.is_water(p):
        land.append(p)
        for dx, dy in self.moves:
          stack.append((x + dx, y + dy))
    return find_box(land)


def get_size(box: Box) -> Point:
  l, t, r, b = box
  return (r - l + 1, b - t + 1)


def find_box(points: list[Point]) -> Box:
  x, y = points[0]
  l = r = x
  t = b = y
  for x, y in points:
    l, r = min(l, x), max(r, x)
    t, b = min(t, y), max(b, y)
  return (l, t, r, b)


# [x] Find all islands
# [x] For each island
# [x]   Show subimage (outlined with red) with padding of TSIZE on all sides
# [x]   If width is not a factor of TSIZE, ask if right or left aligned
# [x]   If height is not a factor of TSIZE, ask if top or bottom aligned
# [x]       Draw colored squares (RGBY) with numbers and ask which square is correct
# [x]   If width or height are larger than TSIZE, split into separate tiles
# [x]   For each tile
# [x]       Prompt for name
# [x]       Add to a primary tile list
# [ ] Output all tile data (name, srcx, srcy, bbox)

# Consider making a new primary image with no blank spaces,
#   Allowing a single index value for lookup


def outline(im: Image.Image, subj: Box, color: str):
  l, t, r, b = subj
  box = (l - 1, t - 1, r + 1, b + 1)
  ImageDraw.Draw(im).rectangle(box, outline=color)


def mod(box: Box, delta: Box) -> Box:
  return tuple([a + b for a, b in zip(box, delta)])


def process(im: Image.Image, orig: Box, all: list[Tile]):
  w, h = im.size
  crop_box = (
      max(0, orig[0] - CROP_PAD),
      max(0, orig[1] - CROP_PAD),
      min(w, orig[2] + CROP_PAD),
      min(h, orig[3] + CROP_PAD),
  )
  subj = (
      orig[0] - crop_box[0],
      orig[1] - crop_box[1],
      orig[2] - crop_box[0],
      orig[3] - crop_box[1],
  )
  crop = im.crop(crop_box)

  alts = []
  subj_w = subj[2] - subj[0] + 1
  subj_h = subj[3] - subj[1] + 1
  hrem = subj_w % TSIZE
  vrem = subj_h % TSIZE
  if hrem:
    alts.append(mod(subj, (-hrem, 0, 0, 0)))
    alts.append(mod(subj, (0, 0, +hrem, 0)))
  if vrem:
    alts = [
        mod(src, delta)
        for src in alts or [subj]
        for delta in [(0, -vrem, 0, 0), (0, 0, 0, +vrem)]
    ]

  if alts:
    opts = ''
    for alt, color in zip(alts, COLORS):
      outline(crop, alt, color)
      opts += color[0]
    crop.show()
    choice = '_'
    while choice not in opts:
      choice = input(f'Which box is correct? [{opts}] ')
    subj = alts[opts.index(choice)]
  else:
    outline(crop, subj, COLORS[0])
    crop.show()

  # TODO: dedup names
  name = input('Tile name: ')
  color = input('Color: ')
  background = input('Background? [y/N] ')
  tiles = []
  for y in range(subj[1], subj[3], TSIZE):
    for x in range(subj[0], subj[2], TSIZE):
      tiles.append({
          'name': '_'.join(name.split()),
          'color': color,
          'background': background in 'yY',
          'srcx': orig[0] + x - subj[0],
          'srcy': orig[1] + y - subj[1],
      })
  if len(tiles) == 1:
    all.append(tiles[0])
  else:
    for i, tile in enumerate(tiles):
      tile['name'] += f'_{i}'
    all.extend(tiles)


if __name__ == '__main__':
  file = argv[1]
  im = Image.open(file)
  px = im.load()

  def is_blank(p: Point) -> bool:
    return px[p][-1] == 0  # type: ignore

  tiles = []
  for island in Islands(*im.size, is_blank).find():
    process(im, island, tiles)
    print('\nAll tiles:\n', json.dumps(tiles))
