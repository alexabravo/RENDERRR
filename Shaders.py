import random 
from Funciones import *
from FuncionesM import *
from FuncionesS import *

def shader1(render, **kwargs):
  w, v, u = kwargs['bar']
  tx, ty = kwargs['texture_coords']
  tcolor = render.active_text.get_color(tx, ty)
  nA, nB, nC = kwargs['varying_normals']

  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + u*iB + v*iC
  r, g, b = tcolor[2] * intensity, tcolor[1] * intensity, tcolor[0] * intensity
  if r < 0:
    r = 0
  if r > 256:
    r = 255

  if b < 0:
    b = 0
  if b > 256:
    b = 255

  if g < 0:
    g = 0
  if g > 256:
    g = 255

  return color(
      int(r),
      int(g),
      int(b)
    )

def shader2(render, **kwargs):
  w, v, u = kwargs['bar']
  tx, ty = kwargs['texture_coords']
  grey = int(ty * 256)
  tcolor = color(grey, 100, 100)
  nA, nB, nC = kwargs['varying_normals']

  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + u*iB + v*iC

  if (intensity>0.85):
    intensity = 1
  elif (intensity>0.60):
    intensity = 0.80
  elif (intensity>0.45):
    intensity = 0.60
  elif (intensity>0.30):
    intensity = 0.45
  elif (intensity>0.15):
    intensity = 0.30
  else:
    intensity = 0

  return color(
      int(tcolor[2] * intensity) if tcolor[2] * intensity > 0 else 0,
      int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
      int(tcolor[0] * intensity) if tcolor[1] * intensity > 0 else 0
    )


def shader3(render, **kwargs):
  w, v, u = kwargs['bar']
  tx, ty = kwargs['texture_coords']
  tcolor = render.active_text.get_color(tx, ty)
  nA, nB, nC = kwargs['varying_normals']

  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = 1
  r, g, b = tcolor[2] * intensity, tcolor[1] * intensity, tcolor[0] * intensity
  if r < 0:
    r = 0
  if r > 256:
    r = 255

  if b < 0:
    b = 0
  if b > 256:
    b = 255

  if g < 0:
    g = 0
  if g > 256:
    g = 255

  return color(
      int(r),
      int(g),
      int(b)
    )

def shader4(render, **kwargs):
  w, v, u = kwargs['bar']
  tx, ty = kwargs['texture_coords']
  grey = int(ty * 256)
  tcolor = color(grey, 100, 100)
  nA, nB, nC = kwargs['varying_normals']

  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + u*iB + v*iC

  if (intensity>0.55):
    intensity = 0.5
  elif (intensity>0.80):
    intensity = 0.60
  elif (intensity>0.45):
    intensity = 0.50
  elif (intensity>0.20):
    intensity = 0.50
  elif (intensity>0.10):
    intensity = 0.30
  else:
    intensity = 0

  return color(
      int(tcolor[2] * intensity) if tcolor[2] * intensity > 0 else 0,
      int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
      int(tcolor[0] * intensity) if tcolor[1] * intensity > 0 else 0
    )

def shader5(render, **kwargs):
  w, v, u = kwargs['bar']
  tx, ty = kwargs['texture_coords']
  tcolor = render.active_text.get_color(tx, ty)
  nA, nB, nC = kwargs['varying_normals']

  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + u*iB + v*iC
  if intensity <= 0:
    r,g,b = 250, 168, 42
  elif intensity <= 0.5:
    r,g,b = 237, 182, 71
  else:
    r,g,b = 242, 208, 102

  return color(
      int(r),
      int(g),
      int(b)
    )


