import numpy as np
class Volume3D:
    def __init__(self, data: np.ndarray):
        self.data = data
        self.shape = data.shape