import glfw
from OpenGL.GL import *
import numpy as np
from pyassimp import load
from common.shader import load_shaders
from common import camera
from common import texture

class Model:
    def __init__(self):
        self._vertex = None
        self._program = None
        self._projection = None
        self._view = None
        self._model = np.matrix(np.identity(4), dtype=np.float32)

    def set_shaders(self, vpath, fpath):
        self._program = load_shaders(vpath, fpath)
        self._projection_id = glGetUniformLocation(self._program, 'P')
        self._view_id= glGetUniformLocation(self._program, 'V')
        self._model_id = glGetUniformLocation(self._program, 'M')
        self._time_id = glGetUniformLocation(self._program, 'time');

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
        glUniform1f(self._time_id, glfw.get_time())

    projection = property(get_projection, set_projection)
    view = property(get_view, set_view)

class Plane(Model):
    def __init__(self,x,y,z,s,rx,ry,rz):
        super().__init__()
        self._translate = np.matrix(np.eye(4), dtype=np.float32)
        self._scale = np.matrix(np.eye(4), dtype=np.float32)
        self._translate[0,3] = x
        self._translate[1,3] = y
        self._translate[2,3] = z
        self._scale[0,0] = self._scale[1,1] = self._scale[2,2] = s
        rotatex = np.matrix(np.eye(4), dtype=np.float32)
        rotatey = np.matrix(np.eye(4), dtype=np.float32)
        rotatez = np.matrix(np.eye(4), dtype=np.float32)
        rotatex[1,1] = rotatex[2,2] = np.cos(rx)
        rotatex[1,2] = -np.sin(rx)
        rotatex[2,1] = np.sin(rx)
        rotatey[0,0] = rotatey[2,2] = np.cos(ry)
        rotatey[0,2] = np.sin(ry)
        rotatey[2,0] = -np.sin(ry)
        rotatez[0,0] = rotatez[1,1] = np.cos(rz)
        rotatez[0,1] = -np.sin(rz)
        rotatez[1,0] = np.sin(rz)
        self._rotate = rotatex * rotatey * rotatez
        self._model = (self._translate * self._rotate * self._scale).T
        self._vertex = np.array([
            -1.0,0.0,-1.0,
            -1.0,0.0,1.0,
            1.0,0.0,1.0,
            1.0,0.0,-1.0,
            ], dtype=np.float32)

        self._index = np.array([
            0,1,2,
            2,3,0,
            ], dtype=np.uint32)

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
        glDrawElements(GL_TRIANGLES, self._index.nbytes, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)

def init():
    if not glfw.init():
        return

    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

def main():
    init()

    window = glfw.create_window(800, 600, "Chapter10", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClearColor(0.3, 0.3, 0.3, 1)

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)

    res_x, res_y = glfw.get_window_size(window)
    cam = camera.Camera(4,4,4,res_x,res_y)

    floor = Plane(0,0,0,4,0,0,0)
    floor.set_shaders('shader_devel.vs', 'shader_devel.fs')

    wall = Plane(0,0,0,4,np.pi/2,0,0)
    wall.set_shaders('shader_devel.vs', 'shader_devel.fs')

    wall2 = Plane(0,0,0,4,0,0,np.pi/2)
    wall2.set_shaders('shader_devel.vs', 'shader_devel.fs')

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cam.controller(window)
        floor.projection = cam.projection
        floor.view = cam.view
        floor.render()

        wall.projection = cam.projection
        wall.view = cam.view
        wall.render()

        wall2.projection = cam.projection
        wall2.view = cam.view
        wall2.render()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
