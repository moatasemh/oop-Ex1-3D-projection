from IsoscelesTriangle import IsoscelesTriangle
from ProjectablePlane import ProjectablePlane
from IsoscelesTrapezoid import IsoscelesTrapezoid




class ShapeFactory:
    @staticmethod
    def create_shape(row: list[float]) -> ProjectablePlane:
        if len(row) == 9:
            return IsoscelesTriangle(row[0:3], row[3:6], row[6:9])
        elif len(row) == 12:
            return IsoscelesTrapezoid(row[0:3], row[3:6], row[6:9], row[9:12])
        else:
            raise ValueError(f"Invalid CSV row length: {len(row)}")