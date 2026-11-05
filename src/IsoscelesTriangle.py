import numpy as np

from ProjectablePlane import ProjectablePlane

class IsoscelesTriangle(ProjectablePlane):
    def __init__(self, a, b, c):
        self.a=np.array(a,dtype=np.float64)
        """float 64 it means that for each number it will save it in 64 bites """
        self.b=np.array(b,dtype=np.float64)
        self.c=np.array(c,dtype=np.float64)
        self._validate_shape()
        self.Dab=np.linalg.norm(self.b - self.a)
        self.Dbc=np.linalg.norm(self.c - self.b)
        self.H=int(round(self.Dab))
        self.W=int(round(self.Dbc))
        self.v_ab = (self.b - self.a) / self.Dab
        self.v_ac = (self.c - self.a) / np.linalg.norm(self.c - self.a)

    def _validate_shape(self):
        """ checking the triangle
        The code calculates the cross product of vectors AB and AC to determine if they form a valid 2D plane.

If the cross product's magnitude is near zero, it raises an error because the points are collinear and cannot form a triangle.
        """
        Dac = np.linalg.norm(self.c - self.a)
        Dab = np.linalg.norm(self.b - self.a)
        cross_prod = np.cross(self.b - self.a, self.c - self.a)
        if np.linalg.norm(cross_prod) / (Dab * Dac) < 1e-5:
            raise ValueError("Invalid triangle: points are collinear")

        if abs(Dab - Dac) >= 1e-3:
            raise ValueError(f" Invalid Triangle : Dab doesn't equal Dac  {Dab} != {Dac} ")

    def get_parameters(self):
        return self.a , self.a , self.v_ab , self.v_ac , self.H , self.W
     # NOTE: in the triangle we have the same start point a that is why we return the self.a twice
