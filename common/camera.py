import numpy as np

#position = np.matrix([x,y,z],dtype=np.float32)
#target = np.matrix([0,0,0],dtype=np.float32)
#up = np.matrix([0,1,0],dtype=np.float32)
#fov = 45.0
#aspect = w/float(h)
#near = 0.1
#far = 100.0

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
