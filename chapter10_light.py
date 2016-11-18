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
        self._light_id = glGetUniformLocation(self._program, 'LightPosition_w');

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

class Sphere(Model):
    def __init__(self):
        super().__init__()

        self._tex = texture.load('res/texture/eye.bmp')
        scene = load('res/model/sphere.obj')
        mesh = scene.meshes[0]
        self._vertex = mesh.vertices
        self._uv = mesh.texturecoords
        self._normal = mesh.normals
        self._index = mesh.faces

        self._vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._vertex.nbytes, self._vertex, GL_STATIC_DRAW)

        self._uv_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._uv_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._uv.nbytes, self._uv, GL_STATIC_DRAW)

        self._normal_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._normal_buffer)
        glBufferData(GL_ARRAY_BUFFER, self._normal.nbytes, self._normal, GL_STATIC_DRAW)

        self._element_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._index.nbytes, self._index, GL_STATIC_DRAW)

    def set_shaders(self, vpath, fpath):
        super().set_shaders(vpath, fpath)
        self._texture_id = glGetUniformLocation(self._program, 'TextureSampler')

    def render(self):
        super().render()

        lightPos = np.array([4,4,4], dtype=np.float32)
        glUniform3f(self._light_id, lightPos[0], lightPos[1], lightPos[2])

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self._tex)
        glUniform1i(self._texture_id, 0)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._uv_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, self._normal_buffer)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_buffer)
        glDrawElements(GL_TRIANGLES, self._index.nbytes, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)

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
    cam = camera.Camera(0,0,2,res_x,res_y)

    eye = Sphere()
    eye.set_shaders('res/glsl/chapter10.vs', 'res/glsl/chapter10.fs')

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cam.controller(window)

        eye.projection = cam.projection
        eye.view = cam.view
        eye.render()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
