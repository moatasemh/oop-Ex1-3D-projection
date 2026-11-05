import pytest
import numpy as np
import time
from ProjectionEngine import ProjectionEngine
from Volume3D import Volume3D
from IsoscelesTrapezoid import IsoscelesTrapezoid

def test_out_of_bounds():
    dummy_volume= Volume3D(np.ones((10,10,10),dtype=np.uint8))
    shape = IsoscelesTrapezoid([100,100,100],[150,100,100],[100,150,100],[150,150,100])
    engine = ProjectionEngine()
    result=engine.project(dummy_volume,shape)
    assert np.all(result==0)

def test_fps_requremnts():
    big_volume = Volume3D(np.zeros((500, 500, 500), dtype=np.uint8)) #big data according to the assignment reqarments
    shape = IsoscelesTrapezoid([0,0,250], [499,0,250], [0,499,250], [499,499,250])
    engine = ProjectionEngine()
    engine.project(big_volume,shape)
    start=time.perf_counter()
    for i in range (10):
        engine.project(big_volume,shape)
    fps=10/(time.perf_counter()-start)
    assert fps>=30.0, f"performance dropped to {fps} FPS"


