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
        if abs(D_a1b - D_a2c) >= 1e-3:
            raise ValueError(f"Invalid Trapezoid: Vectors are not equal length.")
        D_a1a2 = np.linalg.norm(self.a2 - self.a1)
        D_bc = np.linalg.norm(self.c - self.b)
        if D_a1a2 > D_bc+1e-2:
            raise ValueError("Invalid Trapezoid: the small base longer than the big one")
        v1 = self.a2 - self.a1
        v2 = self.b - self.a1
        v3 = self.c - self.a1
        # Scale-invariant coplanarity check
        n1, n2, n3 = np.linalg.norm(v1), np.linalg.norm(v2), np.linalg.norm(v3)
        if n1 > 0 and n2 > 0 and n3 > 0:
            normalized_volume = abs(np.dot(v1 / n1, np.cross(v2 / n2, v3 / n3)))
            if normalized_volume > 1e-2:  # Equivalent to previous check but normalized
                raise ValueError("Invalid Trapezoid: the points are in the same plane")
    def get_parameters(self):
        return self.a1, self.a2, self.v_a1b, self.v_a2c, self.H, self.W