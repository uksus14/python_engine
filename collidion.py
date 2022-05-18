# import pygame as pg
# from random import randint
# pg.init()
# screen_size = [500, 500]
# bg_color = []
# cell_color = [255, 255, 255]
# rev_color = [40, 40, 40]
# handle_color = [141, 85, 36]
# barrel_color = [100, 100, 100]
# size = 1
# rev_width = 35*size
# rev_height = 400*size
# rev_pos = [(screen_size[0]-rev_width)/2, (screen_size[1]-rev_height)/2, rev_width, rev_height]
# barrel_rad = 75*size
# gap = screen_size[1]/50
# muzzle_cen = [screen_size[0]/2, (screen_size[1]-rev_height)/2+gap+barrel_rad/2-gap]
# barrel_cen = [screen_size[0]/2, (rev_pos[1]+barrel_rad+gap)]
# hole_rad = 20*size
# muzzle_rad = hole_rad*1.5
# barrel_angle = 0
# hole_off = barrel_rad/2+gap
# print(hole_off)
# holes2 = [hole.copy() for hole in holes1]
# holes = {False: holes1, True: holes2}
# hset = False
# handle_width = 70
# handle_pos = [(screen_size[0]-handle_width)/2, gap+2*barrel_rad+rev_pos[1], handle_width, rev_height-gap-2*barrel_rad]
# screen = pg.display.set_mode(screen_size)
# screen.fill(bg_color)
# def draw_rev():
#   pg.draw.circle(screen, barrel_color, barrel_cen, barrel_rad)
#   # print(holes[hset])
#   for hole in holes[hset]:
#     if hole[2]:
#       # print(hole)
#       pg.draw.circle(screen, bullet_color["outside"], hole[:2], hole_rad)
#       pg.draw.circle(screen, bullet_color["inside"], hole[:2], hole_rad/3)
#     else: pg.draw.circle(screen, bg_color, hole[:2], hole_rad)
#   pg.draw.ellipse(screen, handle_color, handle_pos)
#   pg.draw.rect(screen, rev_color, rev_pos)
# def shoot():
#   pg.draw.rect(screen, rev_color, rev_pos)
#   pg.draw.ellipse(screen, handle_color, handle_pos)
#   pg.draw.circle(screen, barrel_color, barrel_cen, barrel_rad)
#   for hole in holes[hset]:
#     if hole[2]:
#       pg.draw.circle(screen, bullet_color["outside"], hole[:2], hole_rad)
#       pg.draw.circle(screen, bullet_color["inside"], hole[:2], hole_rad/3)
#     else: pg.draw.circle(screen, bg_color, hole[:2], hole_rad)
#   pg.draw.circle(screen, rev_color, muzzle_cen, muzzle_rad)
  
  
# mode = 0
# stages = [draw_rev, shoot]
# while True:
#   for event in pg.event.get():
  #   if event.type == pg.QUIT: break
  # keys = pg.key.get_pressed()
  # if keys[pg.K_ESCAPE]: break
  # elif keys[pg.K_KP_ENTER] and mode%2==0:
  #   mode+=1
  #   hset = not hset
  # stages[mode%2]()
  # pg.display.update()

import pygame as pg
from math import hypot
pg.init()

# hard settings
allowed_click_offset = 5

# temporary settings
screen = (422, 153)
screen = (600, 400)
fps = 60
class Compare:
  def correct_method(shapes):
    shapes_n = sorted([shape.shape for shape in shapes])
    return getattr(Compare, "_".join(shapes_n))(*shapes)

  def point_point(p1, p2):
    return hypot(p1.x-p2.x, p1.y-p2.y)

  def point_rect(p, rect):
    if p.shape != "rect":
      p, rect = rect, p
    Cent = rect.center
    Exten = list(map(lambda x:x/2, rect.size))
    dx, dy = [max(0, abs(p.x-Cent[j])-Exten[j]) for j in [0,1]]
    return hypot(dx, dy)

  def rect_rect(rect1, rect2):
    Cent1, Cent2 = rect1.center, rect2.center
    Exten1, Exten2 = list(map(lambda x:x/2, rect1.size)), list(map(lambda x:x/2, rect2.size))
    dx, dy = [max(0, abs(Cent1[i]-Cent2[i])-Exten1[i]-Exten2[i]) for i in [0,1]]
    return hypot(dy, dx)

  def circ_rect(circ, rect):
    if circ.shape != "circle":
      circ, rect = rect, circ
    Cent = rect.center
    Exten = list(map(lambda x:x/2, rect.size))
    dx, dy = [max(0, abs(circ.x-Cent[j])-Exten[j]) for j in [0,1]]
    return max(0, hypot(dx, dy)-circ.r)

  def circ_circ(circ1, circ2):
    return max(0, hypot(circ1.x-circ2.x, circ1.y-circ2.y)-circ1.r-circ2.r)

  def circ_point(p, circ):
    return max(0, hypot(p.x-circ.x, p.y-circ.y)-circ.r)

class Rect:
  def __init__(self, x, y):
    self.x1 = min(x)
    self.y1 = min(y)
    self.x2 = max(x)
    self.y2 = max(y)
    self.xs = x
    self.ys = y
    self.center = [(self.x1+self.x2)/2, (self.y1+self.y2)/2]
    self.size = [abs(self.x1-self.x2), abs(self.y1-self.y2)]
    self.shape = "rect"
  def draw(self, color):
    pg.draw.rect(window, color, pg.Rect(self.x1, self.y1, *self.size))
  def change(self, rect):
    self.__init__(*rect)

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.shape = "point"
  def __eq__(self, second):
    dis = False
    shapes = self.shape, second.shape
    dis = Compare.correct_method(shapes)
    return dis <= allowed_click_offset

class Circle:
  def __init__(self, x, y, r):
    self.x = x
    self.y = y
    self.r = r
  def draw(self, color):
    pg.draw.circle(window, color, (self.x, self.y), self.r)
    

window = pg.display.set_mode(screen)
pg.display.set_caption("Set settings")
clock = pg.time.Clock()
buffer = 0
click = False
shapes = [Rect([225, 375], [160, 240]), Rect([225, 375], [160, 240])]
x1, y1 = 0, 0

def update():
  for shape in shapes:
    shape.draw()
  pg.display.flip()
    

while True:
  window.fill((255, 255, 255))
  clock.tick(fps)
  if click:
    x2, y2 = pg.mouse.get_pos()
    shapes[1].change([[x1, x2], [y1, y2]])
  for event in pg.event.get():
    if event.type == pg.QUIT:
      pg.quit()
      run = False
    elif event.type == pg.MOUSEBUTTONDOWN:
      x1, y1 = pg.mouse.get_pos()
      click = True
    elif event.type == pg.MOUSEBUTTONUP:
      print(Compare.correct_method(shapes))
      click = False
  update()
# import os
# import pygame as pg
# from json import dumps, load
# path = __file__.rpartition("\\")[0]
# if not os.path.exists(f"{path}\\additional\\screen.json"):
#   with open(f"{path}\\additional\\screen.json", "w+") as f: pass
# else:
#   with open(f"{path}\\additional\\screen.json", "r") as f:
#     data = load(f)
#     mapp = data["mapp"]
#     grid, deform = data["Icon border"][1]

# stu, ups, mapp, deform, grid = 0, 0, 0, 0, 0
# fps = 60
# # stu = 0.5
# ups = 8

# if not grid:
#   grid = [25, 10]
# if not mapp:
#   mapp = [[0 for _ in range(grid[0])] for _ in range(grid[1])]
# if not deform:
#   deform = [38, 50.5]
# else:
#   deform = [deform[0]/2, deform[1]/2]
# if stu:
#   fpu = fps*stu
# else:
#   fpu = fps/ups

# pg.init()
# window = pg.display.set_mode((grid[0]*deform[0], grid[1]*deform[1]))
# pg.display.set_caption("Set engaged")
# clock = pg.time.Clock()


# window.fill((127, 127, 127))
# run = True
# click = [False, 1]
# tick = 0

# while run:
#   if click[0]:
#     x, y = pg.mouse.get_pos()
#     x, y = int(x/deform[0]), int(y/deform[1])
#     mapp[y][x] = click[1]
#   clock.tick(fps)
#   ev = pg.event.get()
#   for event in ev:
#     if event.type == pg.QUIT:
#       pg.quit()
#       run = False
#     elif event.type == pg.MOUSEBUTTONDOWN:
#       x, y = pg.mouse.get_pos()
#       x, y = int(x/deform[0]), int(y/deform[1])
#       click = [True, abs(mapp[y][x]-1)]
#     elif event.type == pg.MOUSEBUTTONUP:
#       click[0] = False
#   if not run: break
#   for y, row in enumerate(mapp):
#     for x, cell in enumerate(row):
#       pg.draw.rect(window, pg.Color((1-cell)*255, (1-cell)*255, (1-cell)*255), pg.Rect(x*deform[0]+1, y*deform[1]+1, deform[0]-1, deform[1]-1))
#   pg.display.flip()
#   tick += 1
#   if tick <= fpu:
#     continue
#   tick %= fpu
#   jcon = {"mapp": mapp, "Icon border": [[], [grid, [deform[0]*2, deform[1]*2]]]}
#   corners = sum([sum([[(x, y), (x+1, y), (x, y+1), (x+1, y+1)] for x, cell in enumerate(row) if cell], []) for y, row in enumerate(mapp)], [])
#   borders = []
#   for corner in set(corners):
#     if ((corner[0] and corner[1] and corners.count(corner) < 4) or (corner[0] ^ corner[1] and corners.count(corner) < 2)) and corner not in borders:
#       borders.append(corner)
#   poly = []
#   for x, y in borders:
#     for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
#       cx, cy = min(x, x+dx), min(y, y+dy)
#       normx = lambda x: max(min(x, grid[0]-1), 0)
#       normy = lambda y: max(min(y, grid[1]-1), 0)
#       down_border = mapp[normy(y)][normx(cx)]
#       if y == grid[1]: down_border = False
#       if (x+dx, y+dy) in borders and ((dx and (down_border ^ mapp[normy(y-1)][normx(cx)])) or (dy and (mapp[normy(cy)][normx(x)] ^ mapp[normy(cy)][normx(x-1)]))):
#         poly.append(tuple(sorted([(x, y), (x+dx, y+dy)], key=lambda p: 30*p[0]+p[1])))
#   poly = list(set(poly))

#   jcon["Icon border"][0] = poly
#   with open(f"{path}\\additional\\screen.json", "w") as f: f.write(dumps(jcon))

# I WILL clean it up
# later...
