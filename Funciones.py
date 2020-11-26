from Textura import *
from FuncionesM import *
from FuncionesS import *
import math 

blanc = color(255,255,255)

class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.xVP = 0
    self.yVP = 0
    self.hVP = 0
    self.wVP = 0
    self.clear_color = blanc #color(255, 255, 255)
    self.light = V3(0,0,1)
    self.active_text = None
    self.active_shader  = None
    self.active_vert = []
    self.glClear()

  def glClear(self):
    self.buffer = [
      [blanc for x in range(self.width)] 
      for y in range(self.height)
    ]
    self.zbuffer = [
      [-float('inf') for x in range(self.width)] 
      for y in range(self.height)
    ]

  def define_color(self, color):
    self.clear_color = color

  def glColor(self, r=1, g=1, b=1):
    red = round(r*255)
    green = round(g*255)
    blue = round(g*255)
    self.clear_color = color(red, green, blue)

  def glpoint(self, x, y):
    try:
      self.buffer[y][x] = self.clear_color
    except:

      pass
    
  #def glCreateWindow(self, width, height):
        #self.width = width
        #self.height = height
        
  def glLine(self, x0, y0, x1, y1):
    x1, y1 = x0, y0
    x2, y2 = x1, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)
    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0
    threshold = dx

    y = y1
    for x in range(x1, x2 + 1):
        if steep:
            self.point(y, x)
        else:
            self.point(x, y)
        
        offset += dy * 2
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += dx * 2


  def triangle(self):
    A = next(self.active_vert)
    B = next(self.active_vert)
    C = next(self.active_vert)

    if self.active_text:
      tA = next(self.active_vert)
      tB = next(self.active_vert)
      tC = next(self.active_vert)

      nA = next(self.active_vert)
      nB = next(self.active_vert)
      nC = next(self.active_vert)

    xmax, ymax, xmin, ymin = bbox(A, B, C)

    normal = norm(cross(sub(B, A), sub(C, A)))
    intensity = dot(normal, self.light)
    if intensity < 0:
      return

    for x in range(round(xmin), round(xmax) + 1):
      for y in range(round(ymin), round(ymax) + 1):
        P = V2(x, y)
        w, v, u = barycentric(A, B, C, P)
        if w < 0 or v < 0 or u < 0:  
          continue


        if self.active_text:
          tx = tA.x * w + tB.x * u + tC.x * v
          ty = tA.y * w + tB.y * u + tC.y * v

          self.clear_color = self.active_shader(
            self,
            triangle=(A, B, C),
            bar=(w, v, u),
            texture_coords=(tx, ty),
            varying_normals=(nA, nB, nC)
          )
        else:
          self.clear_color = color(round(255 * intensity),0,0)
        
        z = A.z * w + B.z * u + C.z * v
        if x < 0 or y < 0:
          continue

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[y][x]:
          self.glpoint(x, y)
          self.zbuffer[y][x] = z
    
  def transform(self, vert):

    augmented_vertex = [
      [vert.x],
      [vert.y],
      [vert.z],
      [1]
    ]
    
    tran_vert = multiMatriz(self.Viewport, self.Projection) 
    tran_vert = multiMatriz(tran_vert, self.View) 
    tran_vert = multiMatriz(tran_vert, self.Model) 
    tran_vert = multiMatriz(tran_vert, augmented_vertex)

    tran_vert = [
      (tran_vert[0][0]),
      (tran_vert[1][0]),
      (tran_vert[2][0])
    ]
    return V3(*tran_vert)

  def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    self.loadModelMatrix(translate, scale, rotate)
    model = Obj(filename)
    buffer_vert = []

    for face in model.faces:
        vcount = len(face) 
        if vcount == 3:
            for facepart in face:
                vert = self.transform(V3(*model.vertices[facepart[0]-1]))
                buffer_vert.append(vert)

            if self.active_text:
                for facepart in face:
                    tvert = V2(*model.tvertices[facepart[1]-1])
                    buffer_vert.append(tvert)

                for facepart in face:
                    nvert = V3(*model.normals[facepart[2]-1])
                    buffer_vert.append(nvert)
                    
        elif vcount == 4:
            for findex in [0,1,2]:
                facepart = face[findex]
                vert = self.transform(V3(*model.vertices[facepart[0]-1]))
                buffer_vert.append(vert)
            try:
              if self.active_text:
                  for findex in range(0,3):
                      facepart = face[findex]
                      tvert = V2(*model.tvertices[facepart[1]-1])
                      buffer_vert.append(tvert)

                  for faceindex in range(0,3):
                      facepart = face[faceindex]
                      nvert = V3(*model.normals[facepart[2]-1])
                      buffer_vert.append(nvert)
                        
              for findex in [3,0,2]:
                  facepart = face[findex]
                  vert = self.transform(V3(*model.vertices[facepart[0]-1]))
                  buffer_vert.append(vert)

              if self.active_text:
                  for findex in [3,0,2]:
                      facepart = face[findex]
                      tvert = V2(*model.tvertices[facepart[1]-1])
                      buffer_vert.append(tvert)

                  for findex in [3,0,2]:
                      facepart = face[findex]
                      nvert = V3(*model.normals[facepart[2]-1])
                      buffer_vert.append(nvert)
            except:
              pass  
    self.active_vert = iter(buffer_vert)

  def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    translate = V3(*translate)
    scale = V3(*scale)
    rotate = V3(*rotate)

    translation_matrix = [
      [1, 0, 0, translate.x],
      [0, 1, 0, translate.y],
      [0, 0, 1, translate.z],
      [0, 0, 0, 1],
    ]


    a = rotate.x
    rotation_matrix_x = [
      [1, 0, 0, 0], [0, math.cos(a), -math.sin(a), 0],
      [0, math.sin(a),  math.cos(a), 0],[0, 0, 0, 1]
    ]

    a = rotate.y
    rotation_matrix_y = [
      [math.cos(a), 0, math.sin(a), 0], [0, 1, 0, 0],
      [-math.sin(a), 0,  math.cos(a), 0], [0, 0, 0, 1]
    ]

    a = rotate.z
    rotation_matrix_z = [
      [math.cos(a), -math.sin(a), 0, 0],
      [math.sin(a),  math.cos(a), 0, 0],
      [0, 0, 1, 0], [0, 0, 0, 1]
    ]

    rotation_matrix = multiMatriz(rotation_matrix_x, rotation_matrix_y)
    rotation_matrix = multiMatriz(rotation_matrix, rotation_matrix_z)

    scale_matrix = [
      [scale.x, 0, 0, 0],
      [0, scale.y, 0, 0],
      [0, 0, scale.z, 0],
      [0, 0, 0, 1],
    ]

    MultiMatMod = multiMatriz(translation_matrix, rotation_matrix) 
    self.Model = multiMatriz(MultiMatMod, scale_matrix)

  def loadViewMatrix(self, x, y, z, center):
    M = [
      [x.x, x.y, x.z,  0],
      [y.x, y.y, y.z, 0],
      [z.x, z.y, z.z, 0],
      [0, 0, 0, 1]
    ]

    O = [
      [1, 0, 0, -center.x],
      [0, 1, 0, -center.y],
      [0, 0, 1, -center.z],
      [0, 0, 0, 1]
    ]

    self.View = multiMatriz(M, O)

  def loadProjectionMatrix(self, coeff):
    self.Projection =  [
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, coeff, 1]
    ]

  def loadViewportMatrix(self, x = 0, y = 0):
    self.Viewport =  [
      [self.width/2, 0, 0, x + self.width/2],
      [0, self.height/2, 0, y + self.height/2],
      [0, 0, 128, 128],
      [0, 0, 0, 1]
    ]

  def lookAt(self, eye, center, up):
    z = norm(sub(eye, center))
    x = norm(cross(up, z))
    y = norm(cross(z, x))
    self.loadViewMatrix(x, y, z, center)
    self.loadProjectionMatrix(-1 / length(sub(eye, center)))
    self.loadViewportMatrix()

  def draw_arrays(self, polygon):
    if polygon == 'TRIANGLES':
      try:
        while True:
          self.triangle()
      except StopIteration:
        #Mensaje cuando ya se cargo el modelo.
        print('Modelo Listooo')

  def glFinish(self, filename):
    f = open(filename, 'bw')

    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    for x in range(self.height):
      for y in range(self.width):
        f.write(self.buffer[x][y])

    f.close()


  
