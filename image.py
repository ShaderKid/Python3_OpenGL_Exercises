import glfw
from OpenGL.GL import *
import numpy as np
from pyassimp import load
from PIL import Image
from common.shader import load_shaders
from common import camera
from common import texture

def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_S and action == glfw.PRESS and mods == glfw.MOD_SUPER:
        width,height = glfw.get_window_size(window)
        rgb_buffer = glReadPixels(0,0,width,height,GL_RGB,GL_UNSIGNED_BYTE)
        depth_buffer = glReadPixels(0,0,width,height,GL_DEPTH_COMPONENT,GL_UNSIGNED_BYTE)
        rgb_image = Image.frombytes(mode='RGB', size=(width,height), data=rgb_buffer)
        depth_image = Image.frombytes(mode='L', size=(width,height), data=depth_buffer)
        rgb_image = rgb_image.transpose(Image.FLIP_TOP_BOTTOM)
        depth_image = depth_image.transpose(Image.FLIP_TOP_BOTTOM)
        rgb_image.save('rgb.png')
        depth_image.save('depth.png')
        print('保存しました')

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

    window = glfw.create_window(800, 600, "Chapter5", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos(window, 400, 300)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClearColor(0.3, 0.3, 0.3, 1)

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)
    program_id = load_shaders('res/glsl/chapter8.vs', 'res/glsl/chapter8.fs')
    tex = texture.load('res/texture/eye.bmp')
    texture_id = glGetUniformLocation(program_id, 'TextureSampler')

    res_x, res_y = glfw.get_window_size(window)
    cam = camera.Camera(0,0,2,res_x,res_y)
    model = np.matrix(np.identity(4), dtype=np.float32)

    projection_id = glGetUniformLocation(program_id, 'projection')
    view_id = glGetUniformLocation(program_id, 'view')
    model_id = glGetUniformLocation(program_id, 'model')

    scene = load('res/model/sphere.obj')
    mesh = scene.meshes[0]
    vertex = mesh.vertices
    uv = mesh.texturecoords
    normal = mesh.normals
    index = mesh.faces

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)

    uv_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, uv_buffer)
    glBufferData(GL_ARRAY_BUFFER, uv.nbytes, uv, GL_STATIC_DRAW)

    normal_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, normal_buffer)
    glBufferData(GL_ARRAY_BUFFER, normal.nbytes, normal, GL_STATIC_DRAW)

    element_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, GL_STATIC_DRAW)

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cam.controller(window)

        glUseProgram(program_id)
        glUniformMatrix4fv(projection_id, 1, GL_FALSE, cam.projection)
        glUniformMatrix4fv(view_id, 1, GL_FALSE, cam.view)
        glUniformMatrix4fv(model_id, 1, GL_FALSE, model)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)
        glUniform1i(texture_id, 0)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, uv_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, normal_buffer)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)
        glDrawElements(GL_TRIANGLES, index.nbytes, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
