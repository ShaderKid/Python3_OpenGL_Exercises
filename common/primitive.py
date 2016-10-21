import numpy as np

#def grid(w_num: int=1, h_num: int=1) -> np.ndarray:
#    if w_num == 0:
#        w_num = 1
#    if h_num == 0:
#        h_num = 1
#
#    vertex = np.arange(0, (w_num+1+h_num+1)*2, dtype=np.float32)
#    for w in range(w_num+1):
#
#
#    return vertex

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

def sphere(radius,num):
    v = []
    c = []
    index = []
    angle = 2.0 * np.pi / num
    theta = 0.0
    for i in range(num//2+1):
        phi = 0.0
        for j in range(num):
            v.append(radius * np.sin(theta) * np.cos(phi))
            v.append(radius * np.cos(theta))
            v.append(radius * np.sin(theta) * np.sin(phi))

            c.append(0.0)
            c.append(float(i&1))
            c.append(float((i+1)&1))
            phi += angle
        theta += angle

    for i in range(num//2):
        index_y = i * num
        for j in range(num):
            index.append(index_y + j)
            index.append(index_y + num + j)
            index.append(index_y + ((j+1)%num))

            index.append(index_y + ((j+1)%num))
            index.append(index_y + num + j)
            index.append(index_y + num + ((j+1)%num))

    return np.array(v, dtype=np.float32), np.array(c, dtype=np.float32), np.array(index, dtype=np.uint32)

def box():
    r,g,b = np.random.rand(),np.random.rand(),np.random.rand()
    v = np.array([
        # 上
        -0.5,0.5,-0.5,
        -0.5,0.5,0.5,
        0.5,0.5,0.5,
        0.5,0.5,-0.5,

        # 下
        -0.5,-0.5,-0.5,
        -0.5,-0.5,0.5,
        0.5,-0.5,0.5,
        0.5,-0.5,-0.5], dtype=np.float32)

    c = np.array([
        r,g,b,
        r,g,b,
        r,g,b,
        r,g,b,

        r,g,b,
        r,g,b,
        r,g,b,
        r,g,b], dtype=np.float32)

    i = np.array([
        # 上
        0,1,3,
        3,1,2,

        # 下
        7,5,4,
        6,5,7,

        # 後
        3,4,0,
        7,4,3,

        # 前
        1,5,2,
        2,5,6,

        # 左
        0,4,1,
        1,4,5,

        # 右
        2,6,3,
        3,6,7,
        ], dtype=np.uint32)

    return v,c,i
