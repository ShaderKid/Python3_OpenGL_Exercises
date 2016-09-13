import math, numpy

def circle(x=0, y=0, z=0, r=1, v=3):
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

def rect(x=0, y=0, z=0, w=1, h=1):
    vertex = numpy.array(
        [
            x-(w/2), y+(h/2), z,
            x-(w/2), y-(h/2), z,
            x+(w/2), y+(h/2), z,
            x+(w/2), y-(h/2), z,
        ], numpy.float32)
    return vertex
