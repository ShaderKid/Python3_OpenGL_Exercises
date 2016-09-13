import math, numpy

def circle(x: 'x座標(number)'=0, y: 'y座標(number)'=0, z: 'z座標(number)'=0, r: '半径(number)'=1, v: '頂点数(number)'=3) -> numpy.ndarray:
    if (r is 0):
        r = 1
    if (v < 3):
        v = 3

    vertex = numpy.arange(0, (v+2)*3, dtype=numpy.float32)
    vertex[0], vertex[1], vertex[2] = x,y,z

    for i in range(v+1):
        a = 2*math.pi/v*i
        vx = math.cos(a)*r + x
        vy = math.sin(a)*r + y
        vz = 0 + z
        vertex[3*(i+1)+0] = vx
        vertex[3*(i+1)+1] = vy
        vertex[3*(i+1)+2] = vz

    return vertex

def rect(x: 'x座標(number)'=0, y: 'y座標(number)'=0, z: 'z座標(number)'=0, w: '横幅(number)'=1, v: '高さ(number)'=1) -> numpy.ndarray:
    vertex = numpy.array(
        [
            x-(w/2), y+(h/2), z,
            x-(w/2), y-(h/2), z,
            x+(w/2), y+(h/2), z,
            x+(w/2), y-(h/2), z,
        ], numpy.float32)
    return vertex
