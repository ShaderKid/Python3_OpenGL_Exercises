import glfw
from OpenGL.GL import *
import numpy as np
from pyassimp import load
from common.shader import load_shaders
from common import camera, texture, breakout

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

    window = glfw.create_window(800, 800, "3Dブロック崩し", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClearColor(0.3, 0.3, 0.3, 1)

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_id)

    res_x, res_y = glfw.get_window_size(window)
    #projection = camera.perspective(45.0, res_x/res_y, 0.1, 100.0)
    projection = camera.ortho(-1,1,-1,1,0.1,10.0)
    view = camera.look_at(
        np.matrix([0,0,0], dtype=np.float32),
        np.matrix([0,0,-3], dtype=np.float32),
        #np.matrix([0,0,-10], dtype=np.float32),
        np.matrix([0,1,0], dtype=np.float32))
    model = np.matrix(np.identity(4), dtype=np.float32)

    wall = breakout.Wall()
    wall.projection = projection
    wall.view = view
    wall.set_shaders('res/glsl/breakout_wall.vs', 'res/glsl/breakout_wall.fs')

    #blocks = []
    #X_NUM = 5
    #Y_NUM = 5
    #Z_NUM = 5
    #X_SIZE = (2-(X_NUM+1)*0.05)/X_NUM
    #Y_SIZE = (2-(Y_NUM+1)*0.05)/Y_NUM
    #Z_SIZE = X_SIZE
    #for z in range(Z_NUM):
    #    for y in range(Y_NUM):
    #        for x in range(X_NUM):
    #            block = breakout.Block(0.05+X_SIZE/2+x*(X_SIZE+0.05)-1,0.05+Y_SIZE/2+y*(Y_SIZE+0.05)-1,-10+0.05+Z_SIZE/2+z*(Z_SIZE+0.05),X_SIZE,Y_SIZE,X_SIZE)
    #            block.projection = projection
    #            block.view = view
    #            block.set_shaders('res/glsl/breakout_block.vs', 'res/glsl/breakout_block.fs')
    #            blocks.append(block)
    block = breakout.Block(0,0,-3,0.3,0.2,0.4)
    block.projection = projection
    block.view = view
    block.set_shaders('res/glsl/breakout_block.vs', 'res/glsl/breakout_block.fs')

    #ball = breakout.Ball(0,0,-1.5,0.1)
    ball = breakout.Ball(0,0,-3,0.1)
    ball.projection = projection
    ball.view = view
    ball.set_shaders('res/glsl/breakout_ball.vs', 'res/glsl/breakout_ball.fs')

    vx = np.random.rand() / 30 + 0.01
    vy = np.random.rand() / 20 + 0.01
    vz = 0.1

    count_x = 0
    count_y = 0
    count_z = 0
    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        xpos,ypos = glfw.get_cursor_pos(window)
        ball.x = (xpos/res_x)*2-1
        ball.y = (1-ypos/res_y)*2-1
        #ball.z = ((1-ypos/res_y)*2-1)*-1-3
        #ball.x += vx
        #ball.y += vy
        #ball.z += vz

        #if ball.x + ball._radius > 1:
        #    ball.x = 1 - ball._radius
        #    vx *= -1.001
        #elif ball.x - ball._radius < -1:
        #    ball.x = -1 + ball._radius
        #    vx *= -1.001
        #if ball.y + ball._radius > 1:
        #    ball.y = 1 - ball._radius
        #    vy *= -1.001
        #elif ball.y - ball._radius < -1:
        #    ball.y = -1 + ball._radius
        #    vy *= -1.001
        #if ball.z + ball._radius > -1.5:
        #    ball.z = -1.5 - ball._radius
        #    vz *= -1.001
        #elif ball.z - ball._radius < -10:
        #    ball.z = -10 + ball._radius
        #    vz *= -1.001

        #wall.render()

        #new_blocks = []
        #for block in blocks:
        #    block.render()
        #    if (ball.z - ball._radius < block.z + block._d/2) and (block.x-block._w/2 < ball.x < block.x+block._w/2) and (block.y-block._h/2 < ball.y < block.y+block._h/2):
        #        ball.z = block.z + block._d/2
        #        vz *= -1.001
        #    else:
        #        new_blocks.append(block)

        #blocks = new_blocks
        if (block.z - block._d/2 < ball.z - ball._radius < block.z + block._d/2) and (block.x-block._w/2 < ball.x < block.x+block._w/2) and (block.y-block._h/2 < ball.y < block.y+block._h/2) or (block.z - block._d/2 < ball.z + ball._radius < block.z + block._d/2) and (block.x-block._w/2 < ball.x < block.x+block._w/2) and (block.y-block._h/2 < ball.y < block.y+block._h/2):
            count_z += 1
            print('Z-hit',count_z)

        if (block.x - block._w/2 < ball.x - ball._radius < block.x + block._w/2) and (block.z-block._d/2 < ball.z < block.z+block._d/2) and (block.y-block._h/2 < ball.y < block.y+block._h/2) or (block.x - block._w/2 < ball.x + ball._radius < block.x + block._w/2) and (block.z-block._d/2 < ball.z < block.z+block._d/2) and (block.y-block._h/2 < ball.y < block.y+block._h/2):
            count_x += 1
            print('X-hit',count_x)

        if (block.y - block._h/2 < ball.y - ball._radius < block.y + block._h/2) and (block.x-block._w/2 < ball.x < block.x+block._w/2) and (block.z-block._d/2 < ball.z < block.z+block._d/2) or (block.y - block._h/2 < ball.y + ball._radius < block.y + block._h/2) and (block.x-block._w/2 < ball.x < block.x+block._w/2) and (block.z-block._d/2 < ball.z < block.z+block._d/2):
            count_y += 1
            print('Y-hit',count_y)


        block.render()


        ball.render()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
