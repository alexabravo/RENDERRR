from Funciones import *
from Shaders import *

#Tamaño de la pantalla
r = Render(800, 800)
#r.glClear()

#Luz
r.light = V3(0, 1, 1)

#Fondo
t = Texture('./Imagenes/granja.bmp')
r.buffer = t.pixels
r.active_text = t
#Shader
r.active_shader = shader1
#vista
r.lookAt(V3(1, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
r.glFinish('resultado.bmp')

#Perro
t = Texture('./Imagenes/perrito.bmp')
r.active_text = t
r.active_shader = shader1
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./Imagenes/perrito.obj', translate=(-0.5, -0.5, 0), scale=(0.2,0.2,0.2), rotate=(0, 1, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('resultado.bmp')

#Conejo
t = Texture('./Imagenes/conejito.bmp')
r.active_text = t
r.active_shader = shader2
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./Imagenes/conejito.obj', translate=(-0.8, -0.98, 0), scale=(0.2,0.2,0.2), rotate=(0.02, 1.6, -0.1))
r.draw_arrays('TRIANGLES')
r.glFinish('resultado.bmp')

#Pajaro
t = Texture('./Imagenes/pajaro.bmp')
r.active_text = t
r.active_shader = shader3
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./Imagenes/pajaro.obj', translate=(-0.1, 0.6, 0), scale=(0.2,0.2,0.2), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('resultado.bmp')

#Sol
t = Texture('./Imagenes/sol.bmp')
r.active_text = t
r.active_shader = shader5
#En esa posicion porque "esta saliendo el sol" 
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./Imagenes/sol.obj', translate=(-0.1, 0, 0), scale=(0.2,0.2,0.2), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('resultado.bmp')

#Planta
t = Texture('./Imagenes/planta.bmp')
r.active_text = t
#Se ve un poco raro con el shader JAJA
r.active_shader = shader4
r.lookAt(V3(1, 0, 5), V3(-0.8, 0.3, 0), V3(0, 1, 0))
r.load('./Imagenes/planta.obj', translate=(0, 0, 0), scale=(0.2,0.2,0.2), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('resultado.bmp')

