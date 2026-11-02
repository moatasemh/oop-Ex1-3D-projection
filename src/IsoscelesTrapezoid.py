from ProjectablePlane import ProjectablePlane
import numpy as np

class IsoscelesTrapezoid(ProjectablePlane):
    def __init__(self, a1, a2, b, c):
        self.a1 = np.array(a1, dtype=np.float64)
        self.a2 = np.array(a2, dtype=np.float64)
        self.b = np.array(b, dtype=np.float64)
        self.c = np.array(c, dtype=np.float64)

        self._validate_shape()

        self.D_a1b = np.linalg.norm(self.b - self.a1)
        self.Dbc = np.linalg.norm(self.c - self.b)

        self.H = int(round(self.D_a1b))
        self.W = int(round(self.Dbc))

        self.v_a1b = (self.b - self.a1) / self.D_a1b
        self.v_a2c = (self.c - self.a2) / np.linalg.norm(self.c - self.a2)

    def _validate_shape(self):
        """ checking the trapezoid"""
        D_a2c = np.linalg.norm(self.c - self.a2)
        D_a1b = np.linalg.norm(self.b - self.a1)
        if abs(D_a1b - D_a2c) >= 1e-2:
            raise ValueError(f"Invalid Trapezoid: Vectors are not equal length.")

    def get_parameters(self):
        return self.a1, self.a2, self.v_a1b, self.v_a2c, self.H, self.W