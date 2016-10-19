import numpy as np

def circle(x: float=0, y: float=0, z: float=0, r: float=1, v: float=3) -> np.ndarray:
    if (r is 0):
        r = 1
    if (v < 3):
        v = 3

    vertex = np.arange(0, (v+2)*3, dtype=np.float32)
    vertex[0], vertex[1], vertex[2] = x,y,z

    for i in range(v+1):
        a = 2*np.pi/v*i+np.pi/2
        vx = np.cos(a)*r + x
        vy = np.sin(a)*r + y
        vz = 0 + z
        vertex[3*(i+1)+0] = vx
        vertex[3*(i+1)+1] = vy
        vertex[3*(i+1)+2] = vz

    return vertex

def rect(x: float=0, y: float=0, z: float=0, w: float=1, h: float=1) -> np.ndarray:
    vertex = np.array(
        [
            x-(w/2), y+(h/2), z,
            x-(w/2), y-(h/2), z,
            x+(w/2), y+(h/2), z,
            x+(w/2), y-(h/2), z,
        ], np.float32)
    return vertex

def star(x: float=0, y: float=0, z: float=0, r_in: float=0.5, r_out: float=1, v: float=5) -> np.ndarray:
    if (r_in > r_out):
        r_in,r_out = r_out,r_in
    if (v < 3):
        v = 3

    vertex = np.arange(0, (v*2+2)*3, dtype=np.float32)
    vertex[0], vertex[1], vertex[2] = x,y,z

    for i in range(v*2+1):
        a = 2*np.pi/(v*2)*i+np.pi/2
        if i%2 == 0:
            vx = np.cos(a)*r_out + x
            vy = np.sin(a)*r_out + y
        else:
            vx = np.cos(a)*r_in + x
            vy = np.sin(a)*r_in + y
        vz = 0 + z
        vertex[3*(i+1)+0] = vx
        vertex[3*(i+1)+1] = vy
        vertex[3*(i+1)+2] = vz

    return vertex
