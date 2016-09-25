import glfw
from OpenGL.GL import *
import numpy, math
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

def window_resize_callback(window,width,height):
    glViewport(0,0,width,height)

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

    window = glfw.create_window(800, 600, "Chapter6", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glfw.set_key_callback(window, key_callback)
    glfw.set_framebuffer_size_callback(window,window_resize_callback)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glDepthFunc(GL_LESS)
    glClearColor(0.3, 0.3, 0.3, 1)

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)
    program_id = load_shaders('res/glsl/chapter6.vs', 'res/glsl/chapter6.fs')
    tex = texture.load('res/texture/dice.png')
    texture_id = glGetUniformLocation(program_id, "TextureSampler")

    res_x, res_y = glfw.get_window_size(window)
    #projection = camera.ortho(-4,4,-3,3,0.1,10.0)
    projection = camera.perspective(45.0, res_x/res_y, 0.1, 100.0)
    view = camera.look_at(
        numpy.matrix([2,2,2], dtype=numpy.float32),
        numpy.matrix([0,0,0], dtype=numpy.float32),
        numpy.matrix([0,1,0], dtype=numpy.float32))
    model = numpy.matrix(numpy.identity(4), dtype=numpy.float32)
    mvp = projection * view * model

    projection_id = glGetUniformLocation(program_id, 'projection')
    view_id = glGetUniformLocation(program_id, 'view')
    model_id = glGetUniformLocation(program_id, 'model')

    vertex = numpy.array([
        #back
        -1,-1,1,
        1,-1,1,
        1,1,1,
        -1,1,1,
        -1,-1,1,
        1,1,1,

        #bottom
        -1,-1,-1,
        1,-1,-1,
        1,-1,1,
        1,-1,1,
        -1,-1,1,
        -1,-1,-1,

        #right
        1,-1,1,
        1,-1,-1,
        1,1,-1,
        1,1,-1,
        1,1,1,
        1,-1,1,

        #left
        -1,-1,-1,
        -1,-1,1,
        -1,1,-1,
        -1,1,-1,
        -1,-1,1,
        -1,1,1,

        #top
        -1,1,1,
        1,1,1,
        1,1,-1,
        1,1,-1,
        -1,1,-1,
        -1,1,1,

        #front
        1,-1,-1,
        -1,-1,-1,
        -1,1,-1,
        -1,1,-1,
        1,1,-1,
        1,-1,-1,

        ], dtype=numpy.float32)

    uv = numpy.array([
        #back
        0.25, 0.5,
        0.5, 0.5,
        0.5, 0.25,
        0.25, 0.25,
        0.25, 0.5,
        0.5, 0.25,

        #bottom
        0.25, 0.25,
        0.5, 0.25,
        0.5, 0.0,
        0.5, 0.0,
        0.25, 0.0,
        0.25, 0.25,

        #right
        0.0, 0.5,
        0.25, 0.5,
        0.25, 0.25,
        0.25, 0.25,
        0.0, 0.25,
        0.0, 0.5,

        #left
        0.5, 0.5,
        0.75, 0.5,
        0.5, 0.25,
        0.5, 0.25,
        0.75, 0.5,
        0.75, 0.25,

        #top
        0.25, 0.75,
        0.5, 0.75,
        0.5, 0.5,
        0.5, 0.5,
        0.25, 0.5,
        0.25, 0.75,

        #front
        0.75,0.5,
        1.0,0.5,
        1.0,0.25,
        1.0,0.25,
        0.75,0.25,
        0.75,0.5,
        ], dtype=numpy.float32)

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)

    uv_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, uv_buffer)
    glBufferData(GL_ARRAY_BUFFER, uv.nbytes, uv, GL_STATIC_DRAW)

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(program_id)
        glUniformMatrix4fv(projection_id, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_id, 1, GL_FALSE, view)
        glUniformMatrix4fv(model_id, 1, GL_FALSE, model)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)
        glUniform1i(texture_id, 0)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, uv_buffer)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, int(len(vertex)/3))

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
