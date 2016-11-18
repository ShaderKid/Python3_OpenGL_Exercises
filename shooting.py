import glfw
from OpenGL.GL import *
import numpy as np
from pyassimp import load
from common.shader import load_shaders
from common import camera
from common import texture
from common.primitive import Model,Grid,Dragon,Suzanne

class Bullet(Model):
    def __init__(self,x=0,y=0,z=0,w=1,h=1,d=1,direction=np.matrix([0,0,0],dtype=np.float32)):
        super().__init__()
        self.direction = direction
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d

        self.set_shaders('shooting_bullet.vs','shooting_bullet.fs')
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

    def update(self):
        self.x += self.direction[0,0]
        self.y += self.direction[0,1]
        self.z += self.direction[0,2]

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

    grid = Grid(0,0,0,10,10,10,10)

    bullets = []

    def mouse_button_callback(window,button,action,mods):
        if button is glfw.MOUSE_BUTTON_LEFT and action is glfw.PRESS:
            bullets.append(Bullet(x=cam.position[0,0]+cam.direction[0,0],y=cam.position[0,1]+cam.direction[0,1],z=cam.position[0,2]+cam.direction[0,2],direction=cam.direction))

    glfw.set_mouse_button_callback(window,mouse_button_callback)

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cam.controller(window)

        grid.projection = cam.projection
        grid.view = cam.view
        grid.render()

        for index,bullet in enumerate(bullets):
            bullet.update()
            bullet.projection = cam.projection
            bullet.view = cam.view
            bullet.render()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
