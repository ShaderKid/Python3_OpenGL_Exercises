import numpy as np

rotate = np.matrix(np.eye(4), dtype=np.float32)
rotate[0,0] = rotate[1,1] = np.cos(np.pi/2)
rotate[0,1] = -np.sin(np.pi/2)
rotate[1,0] = np.sin(np.pi/2)

scale = np.matrix(np.eye(4), dtype=np.float32)
scale[0,0] = scale[1,1] = scale[2,2] = 2

translate = np.matrix(np.eye(4), dtype=np.float32)
translate[0,3] = translate[1,3] = translate[2,3] = 1

print(rotate)
print(scale)
print(translate)

print(rotate.T)
print(translate.T)

print((translate * rotate * scale).T)
