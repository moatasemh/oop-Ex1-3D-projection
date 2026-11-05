import pytest
from IsoscelesTriangle import IsoscelesTriangle
from IsoscelesTrapezoid import IsoscelesTrapezoid
from ProjectionEngine import ProjectionEngine
from Volume3D import Volume3D
import numpy as np


def test_epsilon_tolerance_validation():
    # Valid isosceles triangle (distances are equal to 111.8)
    base_point = [50.0, 0.0, 0.0]
    b = [0.0, 100.0, 0.0]
    c = [100.0, 100.0, 0.0]

    # 1. Small deviation (0.0005) - should pass silently as it is less than 0.001
    a_small_change = [50.0005, 0.0, 0.0]
    IsoscelesTriangle(a_small_change, b, c)  # Should not raise an error

    # 2. Large deviation (0.005) - must raise an error as it is greater than 0.001
    a_big_change = [50.005, 0.0, 0.0]
    with pytest.raises(ValueError, match="Dab doesn't equal Dac"):
        IsoscelesTriangle(a_big_change, b, c)


def test_vector_change_affects_output():
    """
    Verifies that a microscopic shift of the plane coordinates
    actually changes the resulting 2D image matrix.
    """
    # Create a dummy volume (gradient) to ensure pixel differences
    volume_data = np.arange(256 * 256 * 256, dtype=np.uint32).reshape((256, 256, 256))
    volume_data = (volume_data % 256).astype(np.uint8)  # Ensure values are 0-255
    volume = Volume3D(volume_data)

    # Original plane (Trapezoid)
    a1 = [10.0, 10.0, 100.0]
    b = [10.0, 200.0, 100.0]
    c = [200.0, 200.0, 100.0]
    a2 = [200.0, 10.0, 100.0]
    original_shape = IsoscelesTrapezoid(a1, a2, b, c)

    # Shifted plane (Shifted by 0.002 while maintaining isosceles property)
    a1_shifted = [10.002, 10.0, 100.0]
    a2_shifted = [200.002, 10.0, 100.0]
    shifted_shape = IsoscelesTrapezoid(a1_shifted, a2_shifted, b, c)

    engine = ProjectionEngine()

    # Generate images
    frame_original = engine.project(volume, original_shape)
    frame_shifted = engine.project(volume, shifted_shape)

    # Check if the matrices are different
    difference = np.sum(frame_original != frame_shifted)

    print(f"\n[Sensitivity Test] Pixels changed due to 0.002 shift: {difference}")

    # Assert that a change actually occurred (at least in one pixel)
    assert difference > 0, "Bug detected: The engine ignored the coordinate change!"