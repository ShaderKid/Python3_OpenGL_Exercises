from OpenGL.GL import *
import numpy as np
from pyassimp import load
from .shader import load_shaders

def grid(w_num: int=1, d_num: int=1) -> np.ndarray:
    if w_num == 0:
        w_num = 1
    if d_num == 0:
        d_num = 1

    vertex = np.arange(0, (w_num+1)*(d_num+1)*3, dtype=np.float32)
    index = np.arange(0, (w_num*2)*(d_num+1)*2, dtype=np.uint32)
    size = 1
    cell_w = size / w_num
    cell_d = size / d_num
    for z in range(d_num+1):
        for x in range(w_num+1):
            vertex[z*(3*(w_num+1))+3*x+0] = x*cell_w-size/2
            vertex[z*(3*(w_num+1))+3*x+1] = 0
            vertex[z*(3*(w_num+1))+3*x+2] = z*cell_d-size/2

            if x is not w_num:
                index[z*(2*(w_num))+2*x+0] = z*(w_num+1)+x
                index[z*(2*(w_num))+2*x+1] = z*(w_num+1)+x+1

            if z is not d_num:
                index[z*(2*(w_num+1))+2*x+0+len(index)//2] = z*(w_num+1)+x
                index[z*(2*(w_num+1))+2*x+1+len(index)//2] = (z+1)*(w_num+1)+x

    return vertex,index

def circle(x: float=0, y: float=0, z: float=0, r: float=1, v: float=3) -> np.ndarray:
    if (r is 0):
        r = 1
    if (v < 3):
        v = 3

    vertex = np.arange(0, (v+2)*3, dtype=np.float32)
    vertex[0], vertex[1], vertex[2] = x,y,z

    for i in range(v+1):
        a = 2*np.pi/v*i+np.pi/2
        vx = np.cos(a)*r + x
        vy = np.sin(a)*r + y
        vz = 0 + z
        vertex[3*(i+1)+0] = vx
        vertex[3*(i+1)+1] = vy
        vertex[3*(i+1)+2] = vz

    return vertex

def rect(x: float=0, y: float=0, z: float=0, w: float=1, h: float=1) -> np.ndarray:
    vertex = np.array(
        [
            x-(w/2), y+(h/2), z,
            x-(w/2), y-(h/2), z,
            x+(w/2), y+(h/2), z,
            x+(w/2), y-(h/2), z,
        ], np.float32)
    return vertex

def star(x: float=0, y: float=0, z: float=0, r_in: float=0.5, r_out: float=1, v: float=5) -> np.ndarray:
    if (r_in > r_out):
        r_in,r_out = r_out,r_in
    if (v < 3):
        v = 3

    vertex = np.arange(0, (v*2+2)*3, dtype=np.float32)
    vertex[0], vertex[1], vertex[2] = x,y,z

    for i in range(v*2+1):
        a = 2*np.pi/(v*2)*i+np.pi/2
        if i%2 == 0:
            vx = np.cos(a)*r_out + x
            vy = np.sin(a)*r_out + y
        else:
            vx = np.cos(a)*r_in + x
            vy = np.sin(a)*r_in + y
        vz = 0 + z
        vertex[3*(i+1)+0] = vx
        vertex[3*(i+1)+1] = vy
        vertex[3*(i+1)+2] = vz

    return vertex

def sphere(radius,num):
    v = []
    c = []
    index = []
    angle = 2.0 * np.pi / num
    theta = 0.0
    for i in range(num//2+1):
        phi = 0.0
        for j in range(num):
            v.append(radius * np.sin(theta) * np.cos(phi))
            v.append(radius * np.cos(theta))
            v.append(radius * np.sin(theta) * np.sin(phi))

            c.append(0.0)
            c.append(float(i&1))
            c.append(float((i+1)&1))
            phi += angle
        theta += angle

    for i in range(num//2):
        index_y = i * num
        for j in range(num):
            index.append(index_y + j)
            index.append(index_y + num + j)
            index.append(index_y + ((j+1)%num))

            index.append(index_y + ((j+1)%num))
            index.append(index_y + num + j)
            index.append(index_y + num + ((j+1)%num))

    return np.array(v, dtype=np.float32), np.array(c, dtype=np.float32), np.array(index, dtype=np.uint32)

def box():
    r,g,b = np.random.rand(),np.random.rand(),np.random.rand()
    v = np.array([
        # 上
        -0.5,0.5,-0.5,
        -0.5,0.5,0.5,
        0.5,0.5,0.5,
        0.5,0.5,-0.5,

        # 下
        -0.5,-0.5,-0.5,
        -0.5,-0.5,0.5,
        0.5,-0.5,0.5,
        0.5,-0.5,-0.5], dtype=np.float32)

    c = np.array([
        r,g,b,
        r,g,b,
        r,g,b,
        r,g,b,

        r,g,b,
        r,g,b,
        r,g,b,
        r,g,b], dtype=np.float32)

    i = np.array([
        # 上
        0,1,3,
        3,1,2,

        # 下
        7,5,4,
        6,5,7,

        # 後
        3,4,0,
        7,4,3,

        # 前
        1,5,2,
        2,5,6,

        # 左
        0,4,1,
        1,4,5,

        # 右
        2,6,3,
        3,6,7,
        ], dtype=np.uint32)

    return v,c,i

class Model:
    def __init__(self):
        self._vertex = None
        self._program = None
        self._projection = None
        self._view = None
        self._model = np.matrix(np.identity(4), dtype=np.float32)
        self._translate = np.matrix(np.identity(4), dtype=np.float32)
        self._rotate = np.matrix(np.identity(4), dtype=np.float32)
        self._scale = np.matrix(np.identity(4), dtype=np.float32)

    def set_shaders(self, vpath, fpath):
        self._program = load_shaders(vpath, fpath)
        self._projection_id = glGetUniformLocation(self._program, 'P')
        self._view_id= glGetUniformLocation(self._program, 'V')
        self._model_id = glGetUniformLocation(self._program, 'M')
        self._light_id = glGetUniformLocation(self._program, 'LightPosition_w');

    def get_x(self):
        return self._translate[0,3]

    def set_x(self,x):
        self._translate[0,3] = x
        self._model = (self._translate * self._rotate * self._scale).T

    def get_y(self):
        return self._translate[1,3]

    def set_y(self,y):
        self._translate[1,3] = y
        self._model = (self._translate * self._rotate * self._scale).T

    def get_z(self):
        return self._translate[2,3]

    def set_z(self,z):
        self._translate[2,3] = z
        self._model = (self._translate * self._rotate * self._scale).T

    def get_projection(self):
        return self._projection

    def set_projection(self,p):
        self._projection = p

    def get_view(self):
        return self._view

    def set_view(self,v):
        self._view = v

    def update(self):
        pass

    def render(self):
        glUseProgram(self._program)

        glUniformMatrix4fv(self._projection_id, 1, GL_FALSE, self._projection)
        glUniformMatrix4fv(self._view_id, 1, GL_FALSE, self._view)
        glUniformMatrix4fv(self._model_id, 1, GL_FALSE, self._model)

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)
    projection = property(get_projection, set_projection)
    view = property(get_view, set_view)

class Grid(Model):
    def __init__(self,x,y,z,w,d,w_num,d_num):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.d = d

        self.set_shaders('res/glsl/grid.vs','res/glsl/grid.fs')
        self._vertex, self._index = grid(w_num,d_num)

        self._vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._vertex.nbytes, self._vertex, GL_STATIC_DRAW)

        self._element_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._index.nbytes, self._index, GL_STATIC_DRAW)

    def render(self):
        super().render()

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glDrawElements(GL_LINES, self._index.nbytes, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)

    def get_w(self):
        return self._scale[0,0]

    def set_w(self,w):
        self._scale[0,0] = w
        self._model = (self._translate * self._rotate * self._scale).T

    def get_d(self):
        return self._scale[2,2]

    def set_d(self,d):
        self._scale[2,2] = d
        self._model = (self._translate * self._rotate * self._scale).T

    w = property(get_w,set_w)
    d = property(get_d,set_d)

class Dragon(Model):
    def __init__(self,x,y,z,w,h,d):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d

        self.set_shaders('res/glsl/dragon.vs','res/glsl/dragon.fs')

        scene = load('res/model/dragon.obj')
        self._vertex = scene.meshes[0].vertices
        self._normal = scene.meshes[0].normals
        self._index = scene.meshes[0].faces

        self._vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._vertex.nbytes, self._vertex, GL_STATIC_DRAW)

        self._normal_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._normal_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._normal.nbytes, self._normal, GL_STATIC_DRAW)

        self._element_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._index.nbytes, self._index, GL_STATIC_DRAW)

    def render(self):
        super().render()

        lightPos = np.array([4,4,4], dtype=np.float32)
        glUniform3f(self._light_id, lightPos[0], lightPos[1], lightPos[2])

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._normal_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glDrawElements(GL_TRIANGLES, self._index.nbytes, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

    def get_w(self):
        return self._scale[0,0]

    def set_w(self,w):
        self._scale[0,0] = w
        self._model = (self._translate * self._rotate * self._scale).T

    def get_h(self):
        return self._scale[1,1]

    def set_h(self,h):
        self._scale[1,1] = h
        self._model = (self._translate * self._rotate * self._scale).T

    def get_d(self):
        return self._scale[2,2]

    def set_d(self,d):
        self._scale[2,2] = d
        self._model = (self._translate * self._rotate * self._scale).T

    w = property(get_w,set_w)
    h = property(get_h,set_h)
    d = property(get_d,set_d)
