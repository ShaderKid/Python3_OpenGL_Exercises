from OpenGL.GL import *
import numpy as np
from . import shader

class Model:
    def __init__(self):
        self._vertex = None
        self._program = None
        self._projection = None
        self._view = None
        self._model = np.matrix(np.identity(4), dtype=np.float32)

    def set_shaders(self, vpath, fpath):
        self._program = shader.load_shaders(vpath, fpath)
        self._projection_id = glGetUniformLocation(self._program, 'projection')
        self._view_id= glGetUniformLocation(self._program, 'view')
        self._model_id = glGetUniformLocation(self._program, 'model')

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

    projection = property(get_projection, set_projection)
    view = property(get_view, set_view)

class Wall(Model):
    def __init__(self):
        super().__init__()
        self._vertex = np.array([
            -1,-1,1,
            1,-1,1,
            1,1,1,
            -1,1,1,

            -1,-1,-10,
            1,-1,-10,
            1,1,-10,
            -1,1,-10,
            ], dtype=np.float32)

        self._color = np.array([
            1,1,1,
            1,1,1,
            1,1,1,
            1,1,1,

            0.2,0.2,0.2,
            0.2,0.2,0.2,
            0.2,0.2,0.2,
            0.2,0.2,0.2,
            ], dtype=np.float32)

        self._index = np.array([
            #top
            7,6,2,
            2,3,7,

            #bottom
            0,1,5,
            5,4,0,

            #left
            0,4,7,
            7,3,0,

            #right
            5,1,2,
            2,6,5,

            #front
            1,0,3,
            3,2,1,

            #back
            4,5,6,
            6,7,4,
            ], dtype=np.uint32)

        self._vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._vertex.nbytes, self._vertex, GL_DYNAMIC_DRAW)

        self._color_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._color_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._color.nbytes, self._color, GL_STATIC_DRAW)

        self._element_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._index.nbytes, self._index, GL_STATIC_DRAW)


    def render(self):
        super().render()
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._color_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glDrawElements(GL_TRIANGLES, self._index.nbytes, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

class Block(Model):
    def __init__(self,x,y,z,w,h,d):
        super().__init__()
        self._x = x
        self._y = y
        self._z = z
        self._w = w
        self._h = h
        self._d = d

        self._model[0,0] = self._w
        self._model[1,1] = self._h
        self._model[2,2] = self._d
        self._model[3,0] = self._x
        self._model[3,1] = self._y
        self._model[3,2] = self._z

        self._vertex,self._color,self._index = box()

        self._vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._vertex.nbytes, self._vertex, GL_DYNAMIC_DRAW)

        self._color_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._color_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._color.nbytes, self._color, GL_STATIC_DRAW)

        self._element_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._index.nbytes, self._index, GL_STATIC_DRAW)


    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value

        self._model[3,0] = self._x
        self._model[3,1] = self._y
        self._model[3,2] = self._z

    def get_y(self):
        return self._y

    def set_y(self, value):
        self._y = value

        self._model[3,0] = self._x
        self._model[3,1] = self._y
        self._model[3,2] = self._z

    def get_z(self):
        return self._z

    def set_z(self, value):
        self._z = value

        self._model[3,0] = self._x
        self._model[3,1] = self._y
        self._model[3,2] = self._z

    def update(self):
        pass

    def render(self):
        super().render()
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._color_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glDrawElements(GL_TRIANGLES, self._index.nbytes, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)


class Ball(Model):
    def __init__(self,x,y,z,r):
        super().__init__()
        self._x = x
        self._y = y
        self._z = z
        self._radius = r

        self._model[0,0] = r
        self._model[1,1] = r
        self._model[2,2] = r
        self._model[3,0] = self._x
        self._model[3,1] = self._y
        self._model[3,2] = self._z

        self._vx = 10
        self._vy = 20

        self._vertex,self._color,self._index = sphere(1,36)

        self._vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._vertex.nbytes, self._vertex, GL_DYNAMIC_DRAW)

        self._color_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._color_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._color.nbytes, self._color, GL_STATIC_DRAW)

        self._element_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._index.nbytes, self._index, GL_STATIC_DRAW)


    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value

        self._model[3,0] = self._x
        self._model[3,1] = self._y
        self._model[3,2] = self._z

    def get_y(self):
        return self._y

    def set_y(self, value):
        self._y = value

        self._model[3,0] = self._x
        self._model[3,1] = self._y
        self._model[3,2] = self._z

    def get_z(self):
        return self._z

    def set_z(self, value):
        self._z = value

        self._model[3,0] = self._x
        self._model[3,1] = self._y
        self._model[3,2] = self._z

    def update(self):
        pass

    def render(self):
        super().render()
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._color_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glDrawElements(GL_TRIANGLES, self._index.nbytes, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)

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
