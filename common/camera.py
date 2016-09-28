import numpy as np
import glfw

def perspective(fov, aspect, near, far):
    fov_r = np.radians(fov)
    f = 1.0/np.tan(fov_r/2.0)
    projection = np.matrix(np.identity(4, dtype=np.float32))
    projection[0,0] = f/float(aspect)
    projection[1,1] = f
    projection[2,2] = (far+near)/float(near-far)
    projection[2,3] = -1.0
    projection[3,2] = 2.0*far*near/float(near-far)
    return projection
    '''
    [
        f/float(aspect), 0.0,                          0.0,  0.0,
                    0.0,   f,                          0.0,  0.0,
                    0.0, 0.0,   (far+near)/float(near-far), -1.0,
                    0.0, 0.0, 2.0*far*near/float(near-far),  0.0
    ]
    '''

def ortho(left, right, bottom, top, near, far):
    projection = np.matrix(np.identity(4, dtype=np.float32))
    projection[0,0] = 2.0/float(right-left)
    projection[1,1] = 2.0/float(top-bottom)
    projection[2,2] = -2.0/float(far-near)
    projection[3,0] = -(right+left)/float(right-left)
    projection[3,1] = -(top+bottom)/float(top-bottom)
    projection[3,2] = -(far+near)/float(far-near)
    return projection
    '''
    [
                  2.0/float(right-left),                             0.0,                        0.0, 0.0,
                                    0.0,           2.0/float(top-bottom),                        0.0, 0.0,
                                    0.0,                             0.0,       -2.0/float(far-near), 0.0,
        -(right+left)/float(right-left), -(top+bottom)/float(top-bottom),-(far+near)/float(far-near), 1.0
    ]
    '''

def look_at(position, target, up):
    m = np.matrix(np.identity(4, dtype=np.float32))

    forward = target - position
    norm = np.linalg.norm(forward)
    if 0.0 != norm:
        forward /= norm

    norm = np.linalg.norm(up)
    if 0.0 != norm:
        up /= norm

    side = np.cross(forward, up)
    up = np.cross(side, forward)

    m[0,0] = side[0,0]
    m[1,0] = side[0,1]
    m[2,0] = side[0,2]

    m[0,1] = up[0,0]
    m[1,1] = up[0,1]
    m[2,1] = up[0,2]

    m[0,2] = -forward[0,0]
    m[1,2] = -forward[0,1]
    m[2,2] = -forward[0,2]

    t = np.matrix(np.identity(4, np.float32))
    t[3,0] += -position[0,0]
    t[3,1] += -position[0,1]
    t[3,2] += -position[0,2]

    return t.dot(m)

class Camera:
    def __init__(self, x, y, z, w, h):
        self.__position = np.matrix([x,y,z],dtype=np.float32)
        self.__target = np.matrix([0,0,0],dtype=np.float32)
        self.__up = np.matrix([0,1,0],dtype=np.float32)
        self.__fov = 45.0
        self.__aspect = w/float(h)
        self.__near = 0.1
        self.__far = 100.0
        self.projection = None
        self.view = None
        self.__horizontal_angle = 3.14
        self.__vertical_angle = 0.0
        self.__speed = 3.0
        self.__mouse_speed = 0.001
        self.__last_time = None
        self.__last_xpos = None
        self.__last_ypos = None

    def controller(self,window):
        if self.__last_time is None:
            self.__last_time = glfw.get_time()

        current_time = glfw.get_time()
        delta_time = current_time - self.__last_time
        width,height = glfw.get_window_size(window)
        self.__aspect = width/float(height)
        xpos, ypos = glfw.get_cursor_pos(window)

        if self.__last_xpos is None or self.__last_ypos is None:
            self.__last_xpos, self.__last_ypos = xpos, ypos

        #if not (-0.3 < float(width//2-xpos)/(width/2) < 0.3):
        #    self.__horizontal_angle += self.__mouse_speed * float(width//2 - xpos)/(width/2)
        #if not (-0.3 < float(height//2-ypos)/(height/2) < 0.3):
        #    self.__vertical_angle += self.__mouse_speed *  float(height//2 - ypos)/(height/2)
        #glfw.set_cursor_pos(window, width//2, height//2)
        #self.__horizontal_angle += self.__mouse_speed * float(width//2 - xpos)/(width/2)
        #self.__vertical_angle += self.__mouse_speed * float(height//2 - ypos)/(height/2)
        self.__horizontal_angle += self.__mouse_speed * float(self.__last_xpos - xpos)
        self.__vertical_angle += self.__mouse_speed * float(self.__last_ypos - ypos)

        direction = np.matrix([
            np.cos(self.__vertical_angle) * np.sin(self.__horizontal_angle),
            np.sin(self.__vertical_angle),
            np.cos(self.__vertical_angle) * np.cos(self.__horizontal_angle)
        ], dtype=np.float32)

        right = np.matrix([
            np.sin(self.__horizontal_angle - np.pi/2.0),
            0,
            np.cos(self.__horizontal_angle - np.pi/2.0)
        ], dtype=np.float32)

        self.__up = np.cross(right, direction)

        if glfw.get_key(window, glfw.KEY_DOWN) is glfw.PRESS:
            self.__position -= self.__up * delta_time * self.__speed
        if glfw.get_key(window, glfw.KEY_UP) is glfw.PRESS:
            self.__position += self.__up * delta_time * self.__speed
        if glfw.get_key(window, glfw.KEY_S) is glfw.PRESS:
            self.__position -= direction * delta_time * self.__speed
        if glfw.get_key(window, glfw.KEY_W) is glfw.PRESS:
            self.__position += direction * delta_time * self.__speed
        if glfw.get_key(window, glfw.KEY_A) is glfw.PRESS:
            self.__position -= right * delta_time * self.__speed
        if glfw.get_key(window, glfw.KEY_D) is glfw.PRESS:
            self.__position += right * delta_time * self.__speed
        if glfw.get_key(window, glfw.KEY_I) is glfw.PRESS and self.__fov > 1.0:
            self.__fov -= 1.0
        if glfw.get_key(window, glfw.KEY_O) is glfw.PRESS and self.__fov < 180.0:
            self.__fov += 1.0

        self.__target = self.__position + direction
        self.projection = perspective(self.__fov, self.__aspect, self.__near, self.__far)
        self.view = look_at(self.__position, self.__target, self.__up)

        self.__last_xpos, self.__last_ypos = xpos, ypos
        self.__last_time = current_time
