import pytest
from IsoscelesTriangle import IsoscelesTriangle
from IsoscelesTrapezoid import IsoscelesTrapezoid
from ShapeFactory import ShapeFactory


def test_valid_triangle():
    """Verifies that a valid isosceles triangle is created without errors."""
    # The distance from a to b is 100, and the distance from a to c is also 100
    shape = IsoscelesTriangle([50, 0, 0], [0, 100, 0], [100, 100, 0])
    assert shape.H > 0


def test_invalid_triangle_not_isosceles():
    """Verifies that the system raises a ValueError when sides are not equal."""
    with pytest.raises(ValueError, match="Dab doesn't equal Dac"):
        # Right-angled triangle - distances are not equal (100 != 141.42)
        IsoscelesTriangle([0, 0, 0], [0, 100, 0], [100, 100, 0])


def test_invalid_triangle_collinear():
    """Verifies that the system raises a ValueError when points are collinear."""
    with pytest.raises(ValueError, match="points are collinear"):
        IsoscelesTriangle([0, 0, 0], [10, 10, 10], [20, 20, 20])


def test_factory_creates_correct_shapes():
    """Verifies that the Factory creates the correct objects based on array length."""
    # 9 numbers = triangle
    triangle_coords = [0, 0, 0, 10, 0, 0, 0, 10, 0]
    triangle = ShapeFactory.create_shape(triangle_coords)
    assert isinstance(triangle, IsoscelesTriangle)

    # 12 numbers = trapezoid
    trapezoid_coords = [0, 0, 0, 10, 0, 0, 0, 10, 0, 10, 10, 0]
    trapezoid = ShapeFactory.create_shape(trapezoid_coords)
    assert isinstance(trapezoid, IsoscelesTrapezoid)

def test_invalid_trapezoid_unequal_sides():
    """Verifies that the system raises a ValueError for an invalid trapezoid."""
    with pytest.raises(ValueError, match="Vectors are not equal length"):
        # Left side is longer than the right side
        IsoscelesTrapezoid([0, 0, 0], [10, 0, 0], [0, 100, 0], [20, 100, 0])
