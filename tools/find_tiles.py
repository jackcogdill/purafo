#!/usr/bin/env python3

from PIL import Image, ImageDraw
from sys import argv

TSIZE = 32

file = argv[1]
im = Image.open(file)
iw, ih = im.size
px = im.load()

# [x] Find all islands
# [x] For each island
# [x]   Show subimage (outlined with red) with padding of TSIZE on all sides
# [ ]   If width is not a factor of TSIZE, ask if right or left aligned
# [ ]   If height is not a factor of TSIZE, ask if top or bottom aligned
# [ ]       In either above case, add padding to the aligned side to make a factor of TSIZE
# [ ]   If width or height are larger than TSIZE, split into separate tiles
# [ ]   For each tile
# [ ]       Show same subimage as above, but with specific tile outlined (in blue?)
# [ ]       Prompt for name
# [ ]       Add to a master tile list
# [ ] Print all tile data (name, srcx, srcy, bbox)

n = 0
islands = []
visited = set()
moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def is_blank(x, y):
  return px[x, y][-1] == 0


def explore_island(startx, starty):
  points = []

  q = [(startx, starty)]
  while q:
    x, y = q.pop()  # DFS
    if x < 0 or x >= iw or y < 0 or y >= ih:
      continue
    if (x, y) in visited:
      continue
    visited.add((x, y))
    if not is_blank(x, y):
      points.append((x, y))
      for x0, y0 in moves:
        q.append((x + x0, y + y0))

  left = iw
  right = 0
  top = ih
  bottom = 0
  for x, y in points:
    left = min(left, x)
    right = max(right, x)
    top = min(top, y)
    bottom = max(bottom, y)
  w = right - left + 1
  h = bottom - top + 1
  print('size: [%3d x %3d]' % (w, h))
  return [left, top, w, h]


for x in range(iw):
  for y in range(ih):
    if (x, y) in visited:
      continue
    if is_blank(x, y):
      visited.add((x, y))
      continue
    n += 1
    print('Found island %03d' % n, end=' ')
    box = explore_island(x, y)
    islands.append(box)

for x, y, w, h in islands:
  left = max(0, x - TSIZE)
  upper = max(0, y - TSIZE)
  right = min(iw, x + w + TSIZE)
  lower = min(ih, y + h + TSIZE)
  sub = im.crop((left, upper, right, lower))
  draw = ImageDraw.Draw(sub)
  bbox = [(x - left - 1, y - upper - 1), (x - left + w, y - upper + h)]
  draw.rectangle(bbox, outline='red')
  sub.show()
  input()
