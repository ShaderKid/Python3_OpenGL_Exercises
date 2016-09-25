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

def main():
    init()

    window = glfw.create_window(800, 600, "Chapter5", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.3, 0.3, 0.3, 1)

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)
    program_id = load_shaders('res/glsl/chapter7.vs', 'res/glsl/chapter7.fs')

    res_x, res_y = glfw.get_window_size(window)
    #projection = camera.ortho(-4,4,-3,3,0.1,5.0)
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
        -1,-1,-1,
        1,-1,-1,
        1,1,-1,
        -1,1,-1,

        -1,-1,1,
        1,-1,1,
        1,1,1,
        -1,1,1,
        ], dtype=numpy.float32)

    color = numpy.array([
        0,0,0,
        1,0,0,
        1,1,0,
        1,0,1,
        0,1,0,
        0,1,1,
        0,0,1,
        1,1,1,
        ], dtype=numpy.float32)

    index = numpy.array([
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
        ], dtype=numpy.uint32)

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)

    color_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glBufferData(GL_ARRAY_BUFFER, color.nbytes, color, GL_STATIC_DRAW)

    element_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, GL_STATIC_DRAW)

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(program_id)
        glUniformMatrix4fv(projection_id, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_id, 1, GL_FALSE, view)
        glUniformMatrix4fv(model_id, 1, GL_FALSE, model)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)
        glDrawElements(GL_TRIANGLES, index.nbytes, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
