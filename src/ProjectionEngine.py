from numba import njit
import numpy as np
from ProjectablePlane import ProjectablePlane
from Volume3D import Volume3D

@njit # just in time decrator in numba library to compile this function as C code
def _numba_project_plane(volume_data, start_a1, start_a2, v_ab, v_ac, H, W):
    """
   A fancy C core function. No objects here, just pure mathematics.
   That's what guarantees a run of 30+ FPS even on massive volumes
    """
    E = np.zeros((H, W), dtype=np.uint8)
    shape_x, shape_y, shape_z = volume_data.shape

    # copy used to avoid changing the real cordinats
    curr_a1 = start_a1.copy()
    curr_a2 = start_a2.copy()

    for y in range(H):
        curr_a1 += v_ab
        curr_a2 += v_ac

        diff = curr_a2 - curr_a1
        d12 = np.linalg.norm(diff)

        if d12 < 1e-4:
            continue

        dp = diff / d12
        p = curr_a1.copy()

        for x1 in range(int(d12) + 1):
            vx, vy, vz = int(round(p[0])), int(round(p[1])), int(round(p[2]))

            # Boundary checking (Numba makes it almost as efficient as zero CPU clock cycles)
            v = 0
            if 0 <= vx < shape_x and 0 <= vy < shape_y and 0 <= vz < shape_z:
                v = volume_data[vx, vy, vz]

            x = int(np.floor((W / 2.0) - (d12 / 2.0) + x1))
            if 0 <= x < W:
                E[y, x] = v

            p += dp

    return E


class ProjectionEngine:
    def project(self, volume: Volume3D, plane: ProjectablePlane) -> np.ndarray:
        # getting our parametrs for the algorithm
        a1, a2, v_ab, v_ac, H, W = plane.get_parameters()

        # runing our algorithm function
        return _numba_project_plane(volume.data, a1, a2, v_ab, v_ac, H, W)