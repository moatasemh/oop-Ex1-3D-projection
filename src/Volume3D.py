import numpy as np
class Volume3D:
    def __init__(self, data: np.ndarray):
        self.data = data #saving the Nrrd file
        self.shape = data.shape #saving the size of the 3d matrix by shape parameter (x,y,z)