import glfw
from OpenGL.GL import *
import numpy as np
from common.shader import load_shaders
from common import camera

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

    window = glfw.create_window(800, 600, "Chapter3", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glClearColor(0.3, 0.3, 0.3, 1)

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)
    program_id = load_shaders('res/glsl/chapter3.vs', 'res/glsl/chapter3.fs')

    vertex = np.array([
        0, 1, 0,
        -1, -1, 0,
        1, -1, 0], dtype=np.float32)

    color = np.array([
        1, 0, 0,
        0, 1, 0,
        0, 0, 1], dtype=np.float32)

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)

    color_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glBufferData(GL_ARRAY_BUFFER, color.nbytes, color, GL_STATIC_DRAW)

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(program_id)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, int(len(vertex)/3))
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
