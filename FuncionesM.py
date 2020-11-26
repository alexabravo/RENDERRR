import math
from collections import namedtuple

V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def mul(v0, k):
  return V3(v0.x * k, v0.y * k, v0.z *k)

def cross(v0, v1):
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def bbox(*vertices):

  xs = [ vertices.x for vertices in vertices ]
  ys = [ vertices.y for vertices in vertices ]

  return (max(xs), max(ys), min(xs), min(ys))

def barycentric(A, B, C, P):
  cx, cy, cz = cross(
    V3(B.x - A.x, C.x - A.x, A.x - P.x), 
    V3(B.y - A.y, C.y - A.y, A.y - P.y)
  )

  if abs(cz) < 1:
    return -1, -1, -1   


  u = cx/cz
  v = cy/cz
  w = 1 - (u + v)

  return w, v, u

def norm(v0):
  v0length = length(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def multiMatriz(a, b):
    c = []
    for i in range(0,len(a)):
        temp=[]
        for j in range(0,len(b[0])):
            s = 0
            for k in range(0,len(a[0])):
                s += a[i][k]*b[k][j]
            temp.append(s)
        c.append(temp)

    return c
