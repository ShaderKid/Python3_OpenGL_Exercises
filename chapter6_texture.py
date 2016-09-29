import glfw
from OpenGL.GL import *
import numpy as np
from pyassimp import load
from common.shader import load_shaders
from common import camera
from common import texture

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
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glDepthFunc(GL_LESS)
    glClearColor(0.3, 0.3, 0.3, 1)

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)
    program_id = load_shaders('res/glsl/chapter6.vs', 'res/glsl/chapter6.fs')
    tex = texture.load('res/texture/dice.png')
    texture_id = glGetUniformLocation(program_id, 'TextureSampler')

    res_x, res_y = glfw.get_window_size(window)
    #projection = camera.ortho(-4,4,-3,3,0.1,10.0)
    projection = camera.perspective(45.0, res_x/res_y, 0.1, 100.0)
    view = camera.look_at(
        np.matrix([2,2,2], dtype=np.float32),
        np.matrix([0,0,0], dtype=np.float32),
        np.matrix([0,1,0], dtype=np.float32))
    model = np.matrix(np.identity(4), dtype=np.float32)

    projection_id = glGetUniformLocation(program_id, 'projection')
    view_id = glGetUniformLocation(program_id, 'view')
    model_id = glGetUniformLocation(program_id, 'model')

    vertex = np.array([
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

        ], dtype=np.float32)

    uv = np.array([
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
        ], dtype=np.float32)

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
