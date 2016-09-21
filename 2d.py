import glfw
from OpenGL.GL import *
import numpy, math
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
    glfw.window_hint(glfw.RESIZABLE, False)
    glfw.window_hint(glfw.MAXIMIZED, False)

def main():
    init()

    window = glfw.create_window(800, 600, "Chapter2", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glClearColor(0.3, 0.3, 0.3, 1)

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)
    program_id = load_shaders('res/glsl/2d.vs', 'res/glsl/2d.fs')

    res_x, res_y = glfw.get_window_size(window)
    #projection = camera.perspective(45.0, res_x/res_y, 0.1, 100.0)
    projection = camera.ortho(0, 800, 0, 600, -1.0, 1.0)

    projection_id = glGetUniformLocation(program_id, 'projection')

    vertex = numpy.array([
        400, 310,
        390, 290,
        410, 290,], dtype=numpy.float32)

    color = numpy.array([
        1, 0, 0,
        0, 1, 0,
        0, 0, 1], dtype=numpy.float32)

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    #glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)
    glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_DYNAMIC_DRAW)

    color_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glBufferData(GL_ARRAY_BUFFER, color.nbytes, color, GL_STATIC_DRAW)

    last_time = glfw.get_time()

    vx = 100

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        time = glfw.get_time()
        delta_time = time - last_time
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        vertex[0] = vertex[0] + (delta_time * 1 *  vx)
        vertex[2] = vertex[2] + (delta_time * 1 *  vx)
        vertex[4] = vertex[4] + (delta_time * 1 *  vx)

        glUseProgram(program_id)
        glUniformMatrix4fv(projection_id, 1, GL_FALSE, projection)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, int(len(vertex)/2))

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

        glfw.swap_buffers(window)
        glfw.poll_events()

        last_time = time

    glfw.terminate()

if __name__ == "__main__":
    main()
