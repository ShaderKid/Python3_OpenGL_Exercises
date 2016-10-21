import glfw
from OpenGL.GL import *
import numpy as np
from common.shader import load_shaders
from common import camera
from common.breakout import Ball

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

    window = glfw.create_window(800, 600, "Chapter7", None, None)
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
        np.matrix([0,0,10], dtype=np.float32),
        np.matrix([0,0,0], dtype=np.float32),
        np.matrix([0,1,0], dtype=np.float32))
    model = np.matrix(np.identity(4), dtype=np.float32)

    earth = Ball(0,0,0,1)
    earth.set_projection(projection)
    earth.set_view(view)
    earth.set_shaders('res/glsl/breakout_ball.vs','res/glsl/breakout_ball.fs')

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        rotate = np.matrix(np.eye(4), dtype=np.float32)
        rotate[0,0] = rotate[1,1] = np.cos(np.pi/100)
        rotate[0,1] = -np.sin(np.pi/100)
        rotate[1,0] = np.sin(np.pi/100)
        earth._model *= rotate.T

        earth.render()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
