import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *

def load_shaders(vpath: 'vertex path(str)', fpath: 'fragment path(str)'):
    vs = open(vpath, encoding='utf-8')
    fs = open(fpath, encoding='utf-8')
    vertex = vs.read()
    fragment = fs.read()

    shaderV = compileShader([vertex], GL_VERTEX_SHADER)
    shaderF = compileShader([fragment], GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    if not program:
        raise RunTimeError('glCreateProgram faled!')

    glAttachShader(program, shaderV)
    glAttachShader(program, shaderF)

    glLinkProgram(program)

    linked = glGetProgramiv(program, GL_LINK_STATUS)
    if not linked:
        infoLen = glGetProgramiv(program, GL_INFO_LOG_LENGTH)
        infoLog = ""
        if infoLen > 1:
            infoLog = glGetProgramInfoLog(program, infoLen, None)
        glDeleteProgram(program)
        raise RunTimeError("Error linking program:\n%s\n", infoLog)

    return program
