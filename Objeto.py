import struct
import numpy
from FuncionesS import color

def valid(s, base=10, valido=None):
    try:
        return int(s, base)
    except ValueError:
        return valido
      
class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.tvertices = []      
        self.normals = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    prefix = ''
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vt':
                    self.tvertices.append(list(map(float, value.strip().split(' '))))
                elif prefix == 'vn': 
                    self.normals.append(list(map(float,value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(valid, face.split('/'))) for face in value.split(' ')])         
