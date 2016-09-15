import numpy as np
from common import camera

projection = camera.perspective(45.0, 800/600, 0.1, 100.0)

view = camera.look_at(
    np.matrix([4,3,3], dtype=np.float32),
    np.matrix([0,0,0], dtype=np.float32),
    np.matrix([0,1,0], dtype=np.float32))

model = np.matrix(np.identity(4), dtype=np.float32)

mvp = projection * view * model


print(projection)
print(view)
print(model)
print(mvp)
